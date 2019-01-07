
import sqlite3

connection = sqlite3.connect('VEX.db')
c = connection.cursor()

c.execute('''CREATE TABLE events
	(sku TEXT, key TEXT, program TEXT, name TEXT, start TEXT, end TEXT, season TEXT, divisions TEXT, loc_venue TEXT,
	loc_address1 TEXT, loc_address2 TEXT, loc_city TEXT, loc_region TEXT, loc_postcode TEXT, loc_country TEXT)
	''')

c.execute('''CREATE TABLE teams 
	(number TEXT, program TEXT, team_name TEXT, robot_name TEXT, organisation TEXT,
	city TEXT, region TEXT, country TEXT, grade TEXT, is_registered INTEGER)
	''')

c.execute('''CREATE TABLE matches
	(sku TEXT, division TEXT, round INTEGER, instance INTEGER, matchnum INTEGER, scheduled TEXT, field TEXT, red1 TEXT, red2 TEXT,
	red3 TEXT, redsit TEXT, blue1 TEXT, blue2 TEXT, blue3 TEXT, bluesit TEXT, redscore INTEGER, bluescore INTEGER, scored INTEGER)
	''')

c.execute('''CREATE TABLE rankings
	(sku TEXT, division TEXT, rank TEXT, team TEXT, wins INTEGER, losses INTEGER, ties INTEGER, wp INTEGER, ap INTEGER, sp INTEGER,
	tsrp INTEGER, max_score INTEGER, opr REAL, dpr REAL, ccwm REAL)
	''')

c.execute('CREATE TABLE awards (sku TEXT, name TEXT, team TEXT, qualifies TEXT, `order` TEXT)')

c.execute('CREATE TABLE skills (sku TEXT, type INTEGER, rank INTEGER, team TEXT, attempts INTEGER, score INTEGER)')

c.close()