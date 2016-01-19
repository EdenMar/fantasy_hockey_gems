# Filename: PlayerClasses.py

# from PlayerClasses import *

import os.path
import urllib.request
import datetime



# runs if it's determined that no existing data on players exists
def populateDatabase():

	if not (os.path.isdir("Player Stats")):
		os.makedirs("Player Stats")

	# get the newest statistics
	getDailyStats()

	now = datetime.datetime.now()
	
	with open("Daily Stats/" + now) as f:
		data = json.load(f)

	# all JSON data loaded in here; unordered list
	skaterData = data['data']	

	for player in skaterData:
		name = player['playerName']
		gamesPlayed = player['gamesPlayed']
		goals = player['goals']
		assists = player['assists']
		points = player['points']
		plusMinus = player['plusMinus']
		penaltyMinutes = player['penaltyMinutes']
		ppPoints = player['ppPoints']
		ppGoals = player['ppGoals']
		shots = player['shots']
		f = open("Player Stats" + name + ".json")



	return


# downloads the daily stats 
# https://docs.python.org/3/library/os.path.html
# https://docs.python.org/3/library/urllib.request.html#examples
# 

def getDailyStats():

	if not (os.path.isdir("Daily Stats")):
		os.makedirs("Daily Stats")


	now = datetime.datetime.now()
	skaterFile = now.date().isoformat() + " Player Stats"
	goalieFile = now.date().isoformat() + " Goalie Stats"

	if not (os.path.isfile("Daily Stats/" + skaterFile)):	

		skaters = "http://www.nhl.com/stats/rest/grouped/skaters/season/skatersummary?cayenneExp=seasonId=20152016%20and%20gameTypeId=2"

		try:

			with urllib.request.urlopen(skaters) as response:
				data = response.read()

			text = data.decode('utf-8')
			f = open("Daily Stats/" + skaterFile, "w")
			f.write(text)
			f.close()

		except Exception as e:
			print(e)
			raise

	if not (os.path.isfile("Daily Stats/" + goalieFile)):

		goalies = "http://www.nhl.com/stats/rest/grouped/goalies/season/goaliesummary?cayenneExp=seasonId=20152016 and gameTypeId=2 and playerPositionCode="G""	

		try:
			with urllib.request.urlopen(goalies) as response:
				data = response.read()

			text = data.decode('utf-8')
			f = open("Daily Stats/" + goalieFile, "w")
			f.write(text)
			f.close()	

		except Exception as e:
			print(e)
			raise

	return

