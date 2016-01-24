# Filename: PlayerClasses.py

# from PlayerClasses import *

import os.path
import urllib.request
import datetime



# updates and creates a database of individual player stats
def updateDatabase():


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
		if not os.path.isfile("Player Stats/" + name + ".json"):

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
			with open("Player Stats/" + name + ".json", "w") as outfile:
				json.dump(outputData, outfile)

			outfile.close()

		# data exists, but update it
		else:

			with open("Player Stats/" + name + ".json") as statsFile:
				playerStats = json.load(statsFile)

			name = playerStats['playerName']
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
				playerStats['goals']['last 3']			

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

