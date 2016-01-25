# Filename: PlayerClasses.py

# from PlayerClasses import *

import os.path
import urllib.request
import datetime
import json



# updates and creates a database of individual player stats
def updateDatabase():


	if not (os.path.isdir("Player Stats")):
		os.makedirs("Player Stats")

	# get the newest statistics
	getDailyStats()

	now = datetime.date.today()
	
	with open("Daily Stats/" + now.isoformat() + " Player Stats") as f:
		data = json.load(f)

	f.close()

	with open("Daily Stats/" + now.isoformat() + " Goalie Stats") as f2:
		data2 = json.load(f2)

	f2.close()

	# all JSON data loaded in here; unordered list
	skaterData = data['data']
	goalieData = data2['data']	

	for player in skaterData:

		playerName = player['playerName']
		gamesPlayedNew = player['gamesPlayed']
		goalsNew = player['goals']
		assistsNew = player['assists']
		pointsNew = player['points']
		plusMinusNew = player['plusMinus']
		penaltyMinutesNew = player['penaltyMinutes']
		ppPointsNew = player['ppPoints']
		ppGoalsNew = player['ppGoals']
		shGoalsNew = player['shGoals']
		shotsNew = player['shots']

		# if a json file of that player doesn't exist, create it
		if not os.path.isfile("Player Stats/" + playerName + ".json"):

			# https://docs.python.org/3/library/json.html
			# http://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file-in-python
			# b = json.dumps({'playerName':name, 'gamesPlayed':gamesPlayed, 'goals':{'last 3':[goals] + []}})
			outputData = {	
			"playerName": playerName,
			"gamesPlayed" : gamesPlayedNew,
			"goals" : {"last 3": [goalsNew, 0, 0],
						"last 5" : [goalsNew, 0, 0, 0, 0],
						"last 10" : [goalsNew, 0, 0, 0, 0, 0, 0, 0, 0, 0],
						"total" : goalsNew
						}
					,
			"assists" : {"last 3" : [assistsNew, 0, 0],
						"last 5" : [assistsNew, 0, 0, 0, 0],
						"last 10" : [assistsNew, 0, 0, 0, 0, 0, 0, 0, 0, 0],
						"total" : assistsNew
						},		
			"points" : {"last 3" : [pointsNew, 0, 0],
						"last 5" : [pointsNew, 0, 0, 0, 0],
						"last 10" : [pointsNew, 0, 0, 0, 0, 0, 0, 0, 0, 0],
						"total" : pointsNew
						},
			"plusMinus" : plusMinusNew,
			"penaltyMinutes" : penaltyMinutesNew, 
			"ppPoints" : {"last 5" : [ppPointsNew, 0, 0, 0, 0], 
						  "total" : [ppPointsNew, 0, 0, 0, 0, 0, 0, 0, 0, 0]
						  },
			"ppGoals" : {"last 5" : [ppGoalsNew, 0, 0, 0, 0],
						"total": ppGoalsNew
						},
			"shGoals" : {"total" : shGoalsNew
						},			
			"shots" : shotsNew
			}
			with open("Player Stats/" + playerName + ".json", "w") as outfile:
				json.dump(outputData, outfile)

			outfile.close()

		# data exists, but update it
		else:

			with open("Player Stats/" + playerName + ".json") as statsFile:
				playerStats = json.load(statsFile)

			statsFile.close()

			gamesPlayedOld = playerStats['gamesPlayed']
			#dict
			goalsOld = playerStats['goals']
			#dict
			assistsOld = playerStats['assists']
			#dict
			pointsOld = playerStats['points']
			plusMinusOld = playerStats['plusMinus']
			penaltyMinutesOld = playerStats['penaltyMinutes']
			#dict
			ppPointsOld = playerStats['ppPoints']
			#dict
			ppGoalsOld = playerStats['ppGoals']
			shGoalsOld = playerStats['shGoals']
			shotsOld = playerStats['shots']	

			if (gamesPlayedOld == gamesPlayedNew):
				pass

			else:

				playerStats['gamesPlayed'] = gamesPlayedNew

				tmp = goalsNew - playerStats['goals']['total']
				playerStats['goals']['last 3'] = [tmp] + playerStats['goals']['last 3'][:2]
				playerStats['goals']['last 5'] = [tmp] + playerStats['goals']['last 5'][:4]
				playerStats['goals']['last 10'] = [tmp] + playerStats['goals']['last 10'][:9]
				playerStats['goals']['total'] = goalsNew

				tmp = assistsNew - playerStats['assists']['total']
				playerStats['assists']['last 3'] = [tmp] + playerStats['assists']['last 3'][:2]
				playerStats['assists']['last 5'] = [tmp] + playerStats['assists']['last 5'][:4]
				playerStats['assists']['last 10'] = [tmp] + playerStats['assists']['last 10'][:9]
				playerStats['assists']['total'] = assistsNew				

				tmp = pointsNew - playerStats['points']['total']
				playerStats['points']['last 3'] = [tmp] + playerStats['points']['last 3'][:2]
				playerStats['points']['last 5'] = [tmp] + playerStats['points']['last 5'][:4]
				playerStats['points']['last 10'] = [tmp] + playerStats['points']['last 10'][:9]
				playerStats['points']['total'] = pointsNew

				playerStats['plusMinus'] = plusMinusNew
				playerStats['penaltyMinutes'] = penaltyMinutesNew

				tmp = ppPointsNew - playerStats['ppPoints']['total']
				playerStats['ppPoints']['last 5'] = [tmp] + playerStats['ppPoints']['last 5'][:4]
				playerStats['ppPoints']['total'] = ppPointsNew

				tmp = ppGoalsNew - playerStats['ppGoals']['total']
				playerStats['ppGoals']['last 5'] = [tmp] + playerStats['ppGoals']['last 5'][:4]
				playerStats['ppGoals']['total'] = ppGoalsNew

				playerStats['shGoals'] = shGoalsNew
				playerStats['shots'] = shotsNew

				with open("Player Stats/" + name + ".json", "w") as statsFile:
					json.dump(playerStats, statsFile)

				statsFile.close()					


	# for goalie in goalieData:
		

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

		goalies = "http://www.nhl.com/stats/rest/grouped/goalies/season/goaliesummary?cayenneExp=seasonId=20152016%20and%20gameTypeId=2%20and%20playerPositionCode=%22G%22"	

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

def generateDailyReport():

	biggest3Goals = {}
	biggest5Goals = {}
	biggest10Goals = {}
	biggest3Assists = {}
	biggest5Assists = {}
	biggest10Assists = {}
	biggest5Points = {}
	biggest10Points = {}
	biggest3Points = {}

	if not (os.path.isdir("Daily Reports")):
		os.makedirs("Daily Reports")


	return