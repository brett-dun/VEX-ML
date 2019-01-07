
from deprecated import deprecated

import numpy as np


class Team(object):

    def __init__(self, number: str):

        # team number
        self.number = number

        # lists to store points for an against for each match
        self.pointsFor = []
        self.pointsAgainst = []

        # floating point values of average points scored for and against
        self.averagePointsFor = 0.
        self.averagePointsAgainst = 0.

        # lists of the teams that the current team has played with
        self.teammates = []
        # self.opponents = []

        # estimation of a team's actual contribution to the score of the match
        self.estimated_contributions_for = []

        self.average_estimated_contribution_for = 0.

    def add_scores(self, points_for: int, points_against: int) -> None:

        # append new values to the list
        self.pointsFor.append(points_for)
        self.pointsAgainst.append(points_against)

        # update average points for as each score gets added
        self.averagePointsFor = np.mean(self.pointsFor)
        # self.averagePointsFor = (self.averagePointsFor * (len(self.pointsFor)-1) + self.pointsFor[-1]) / len(self.pointsFor)

        # update average points against as each score gets added
        self.averagePointsAgainst = np.mean(self.pointsAgainst)
        # self.averagePointsAgainst = (self.averagePointsAgainst * (len(self.pointsAgainst)-1) + self.pointsAgainst[-1]) / len(self.pointsAgainst)

    def add_teammate(self, team: str) -> None:

        self.teammates.append(team)

    @deprecated(reason="implemented in main method instead")
    def calculate_estimated_contribution(self, teams):

        # print(len(self.pointsFor))
        # print(len(self.teammates))

        for i in range(len(self.pointsFor)):
            self.estimated_contribution_to_score.append(self.pointsFor[i]-teams[self.teammates[i]].averagePointsFor)

    @deprecated(reason="add_scores now does this calculation")
    def calculate_average_points_for(self):
        if len(self.pointsFor) == 0:
            self.averagePointsFor = 0.
        else:
            tot = 0.
            for x in self.pointsFor:
                tot += x
            self.averagePointsFor = tot / len(self.pointsFor)
        return self.averagePointsFor

    @deprecated(reason="add_scores now does this calculation")
    def calculate_average_points_against(self):
        if len(self.pointsAgainst) == 0:
            self.averagePointsFor = 0.
        else:
            tot = 0.
            for x in self.pointsAgainst:
                tot += x
            self.averagePointsAgainst = tot / len(self.pointsAgainst)
        return self.averagePointsFor


''' 
avrg_vals = {}
matc = [[]]
matcLoss = [[]]
avrg = {}
diff_vals = {}
diff = {}
diffLoss_vals = {}
diffLoss = {}
avrg_diff = {}
'''