
"""
    author: Brett Duncan
    python version: 3.6.4
    operation system: Mac OS 10.14.1
"""

from keras.models import Sequential
from keras.layers import Dense

import sqlite3

import numpy as np

from team import *

# https://keras.io/callbacks/#usage-of-callbacks


def main():

    # connect to the sqlite3 database
    connection = sqlite3.connect('VEX.db')

    # get the cursor object
    cursor = connection.cursor()

    # cursor.execute("SELECT * FROM matches WHERE `scored`=1 AND sku IN (SELECT `sku` FROM events WHERE `season`='In The Zone')")

    # execute the command to get data from the database
    cursor.execute("SELECT red1,red2,red3,redsit,blue1,blue2,blue3,bluesit,redscore,bluescore FROM matches WHERE `scored`=1 AND sku IN (SELECT `sku` FROM events WHERE `season`='In The Zone')")

    # get the list from the cursor object
    matches = cursor.fetchall()

    # close the connection with the database
    connection.close()

    # dictionary of Team objects
    teams = {}

    # list containing the match data that I want to use for analysis
    relevant_match_data = []

    # the highest score by any alliance (used for bounding the data between 0 and 1 later)
    max_score = 0

    # iterate through the enumerated match data
    for i, (red1, red2, red3, redsit, blue1, blue2, blue3, bluesit, redscore, bluescore) in enumerate(matches):

        # handle elimination rounds where the third alliance partner may be in instead of one of the other teams
        r1 = red1 if red1 != redsit else red3
        r2 = red2 if red2 != redsit else red3

        b1 = blue1 if blue1 != bluesit else blue3
        b2 = blue2 if blue2 != bluesit else blue3

        # check if the team is in the list of teams
        if r1 not in teams:
            teams[r1] = Team(r1)
        if r2 not in teams:
            teams[r2] = Team(r2)

        if b1 not in teams:
            teams[b1] = Team(b1)
        if b2 not in teams:
            teams[b2] = Team(b2)

        # limit the training data to 75% of the data
        if i < len(matches)*3//4:

            teams[r1].add_scores(redscore, bluescore)
            teams[r1].add_teammate(r2)
            teams[r2].add_scores(redscore, bluescore)
            teams[r2].add_teammate(r1)

            teams[b1].add_scores(redscore, bluescore)
            teams[b1].add_teammate(b2)
            teams[b2].add_scores(redscore, bluescore)
            teams[b2].add_teammate(b1)

        # red wins
        if redscore > bluescore:
            relevant_match_data.append((r1, r2, b1, b2, 1., 0.))
        # blue wins
        elif redscore < bluescore:
            relevant_match_data.append((r1, r2, b1, b2, 0., 1.))
        # tie
        else:
            relevant_match_data.append((r1, r2, b1, b2, 0.5, 0.5))

        # set the max score to a higher score if necessary
        if redscore > max_score:
            max_score = redscore
        if bluescore > max_score:
            max_score = bluescore

    print(len(matches))

    max_contribution = 0.
    min_contribution = 0.

    for team_name, team in teams.items():

        # print(team)

        for i in range(len(team.pointsFor)):

            points_for = team.pointsFor[i]
            partner_average = teams[team.teammates[i]].averagePointsFor
            contribution = points_for - partner_average

            team.estimated_contributions_for.append(contribution)

            if contribution > max_contribution:
                max_contribution = contribution
            if contribution < min_contribution:
                min_contribution = contribution

        tot = 0.
        for x in team.estimated_contributions_for:
            tot += x

        if len(team.estimated_contributions_for) != 0:
            team.average_estimated_contribution_for = tot / len(team.estimated_contributions_for)

        # team.calculate_estimated_contribution(teams)

    '''
    8 columns, len(matches) rows, 64-bit floating point
    [x][0] = average points for red 1
    [x][1] = average points against red 1
    
    [x][2] = average points for red 2
    [x][3] = average points against red 2
    
    [x][4] = average points for blue 1
    [x][5] = average points against blue 1
    
    [x][6] = average points for blue 2
    [x][7] = average points against blue 2
    
    '''
    x_data = np.zeros((len(matches), 12), dtype=np.float64)
    y_data = np.zeros((len(matches), 2), dtype=np.float64)

    # print(data[0])

    # iterate through the enumerated relevant match data
    for i, (r1, r2, b1, b2, red_win, blue_win) in enumerate(relevant_match_data):

        """
        x_data[i][0] = teams[r1].calculate_average_points_for() / max_score
        x_data[i][1] = -teams[r1].calculate_average_points_against() / max_score

        x_data[i][2] = teams[r2].calculate_average_points_for() / max_score
        x_data[i][3] = -teams[r2].calculate_average_points_against() / max_score

        x_data[i][4] = teams[b1].calculate_average_points_for() / max_score
        x_data[i][5] = -teams[b1].calculate_average_points_against() / max_score

        x_data[i][6] = teams[b2].calculate_average_points_for() / max_score
        x_data[i][7] = -teams[b2].calculate_average_points_against() / max_score
        """

        # scale input values to [0,1]
        x_data[i][0] = teams[r1].averagePointsFor / max_score
        x_data[i][1] = teams[r1].averagePointsAgainst / max_score
        x_data[i][2] = (teams[r1].average_estimated_contribution_for - min_contribution) / (max_contribution - min_contribution)

        x_data[i][3] = teams[r2].averagePointsFor / max_score
        x_data[i][4] = teams[r2].averagePointsAgainst / max_score
        x_data[i][5] = (teams[r2].average_estimated_contribution_for - min_contribution) / (max_contribution - min_contribution)

        x_data[i][6] = teams[b1].averagePointsFor / max_score
        x_data[i][7] = teams[b1].averagePointsAgainst / max_score
        x_data[i][8] = (teams[b1].average_estimated_contribution_for - min_contribution) / (max_contribution - min_contribution)

        x_data[i][9] = teams[b2].averagePointsFor / max_score
        x_data[i][10] = teams[b2].averagePointsAgainst / max_score
        x_data[i][11] = (teams[b2].average_estimated_contribution_for - min_contribution) / (max_contribution - min_contribution)

        # output values (who wins)
        y_data[i][0] = red_win
        y_data[i][1] = blue_win

    # define the Keras model
    model = Sequential()

    # add a elu layer
    model.add(Dense(units=12, activation='elu', input_dim=12))

    # model.add(Dense(units=6, activation='elu'))
    # model.add(Dense(units=4, activation='sigmoid'))

    # add a sigmoid function output layer
    model.add(Dense(units=2, activation='sigmoid'))

    # compile model
    model.compile(loss='categorical_crossentropy',
                  optimizer='sgd',
                  metrics=['accuracy'])

    # print('fitting')

    # train the model
    model.fit(x_data[:(len(matches)*3//4)-1], y_data[0:(len(matches)*3//4)-1], epochs=5)

    # get metrics from verification data
    loss_and_metrics = model.evaluate(x_data[(len(matches)*3//4):], y_data[(len(matches)*3//4):])

    print(loss_and_metrics)


if __name__ == "__main__":
    main()
