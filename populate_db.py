
import json
import sqlite3

connection = sqlite3.connect('VEX.db')
cur = connection.cursor()


with open('json files/events.json', 'r') as file:
	data = json.load(file)
	temp = []
	for item in data['result']:
		#find a better way to handle the list of divisions (possibly a csv styled string)
		temp.append([item['sku'], item['key'], item['program'], item['name'], item['start'], item['end'], item['season'], str(item['divisions']),  item['loc_venue'], item['loc_address1'], item['loc_address2'], item['loc_city'], item['loc_region'], item['loc_postcode'], item['loc_country']])
	cur.executemany('INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', temp)
	connection.commit()
print('events complete')


with open('json files/teams.json', 'r') as file:
	data = json.load(file)
	temp = []
	for item in data['result']:
		temp.append([item['number'], item['program'], item['team_name'], item['robot_name'], item['organisation'], item['city'], item['region'], item['country'], item['grade'], item['is_registered']])
	cur.executemany('INSERT INTO teams VALUES (?,?,?,?,?,?,?,?,?,?)', temp)
	connection.commit()
print('teams complete')


with open('json files/matches.json', 'r') as file:
	data = json.load(file)
	temp = []
	for item in data['result']:
		temp.append([item['sku'], item['division'], item['round'], item['instance'], item['matchnum'], item['scheduled'], item['field'], item['red1'],  item['red2'], item['red3'], item['redsit'], item['blue1'], item['blue2'], item['blue3'], item['bluesit'], item['redscore'], item['bluescore'], item['scored']])
	cur.executemany('INSERT INTO matches VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', temp)
	connection.commit()
print('matches complete')


with open('json files/rankings.json', 'r') as file:
	data = json.load(file)
	temp = []
	for item in data['result']:
		temp.append([item['sku'], item['division'], item['rank'], item['team'], item['wins'], item['losses'], item['ties'], item['wp'],  item['ap'], item['sp'], item['trsp'], item['max_score'], item['opr'], item['dpr'], item['ccwm']])
	cur.executemany('INSERT INTO rankings VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', temp)
	connection.commit()
print('rankings complete')


with open('json files/awards.json', 'r') as file:
	data = json.load(file)
	temp = []
	for item in data['result']:
		print(item)
		#find a better way to handle the list of divisions (possibly a csv styled string)
		temp.append([item['sku'], item['name'], item['team'], str(item['qualifies']), item['order']])
	cur.executemany('INSERT INTO awards VALUES (?,?,?,?,?)', temp)
	connection.commit()
print('awards complete')


with open('json files/skills.json', 'r') as file:
	data = json.load(file)
	temp = []
	for item in data['result']:
		temp.append([item['sku'], item['type'], item['rank'], item['team'], item['attempts'], item['score']])
	cur.executemany('INSERT INTO skills VALUES (?,?,?,?,?,?)', temp)
	connection.commit()
print('skills complete')

connection.close()