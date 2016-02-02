
import os.path
import urllib.request
import datetime
import json
import statistics
import csv


# updates and creates a database of individual player stats
def updateDatabase():


	if not (os.path.isdir("Player Stats")):
		os.makedirs("Player Stats")

	# get the newest statistics
	getDailyStats()

	now = datetime.date.today()

	#""
	with open("Daily Stats/" + now.isoformat() + " Player Stats") as f:
		data = json.load(f)

	#""
	with open("Daily Stats/" + now.isoformat() + " Goalie Stats") as f2:
		data2 = json.load(f2)


	# all JSON data loaded in here; unordered list
	skaterData = data['data']
	goalieData = data2['data']	

	"""This for loop parses through the forward and defensemen positions and their stats"""

	for player in skaterData:

		playerName = player['playerName']
		gamesPlayedNew = player['gamesPlayed']
		playerPositionCode = player['playerPositionCode']
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
			outputData = {	
			"playerName": playerName,
			"gamesPlayed" : gamesPlayedNew,
			"playerPositionCode" : playerPositionCode,
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
			"plusMinus" : {"last 3" : [plusMinusNew, 0, 0],
							"last 5" : [plusMinusNew, 0, 0, 0, 0],
							"last 10" : [plusMinusNew, 0, 0, 0, 0, 0, 0, 0, 0, 0]
						"total" : plusMinusNew
						},
			"penaltyMinutes" : {"last 3" : [penaltyMinutesNew, 0, 0],
								"last 5" : [penaltyMinutesNew, 0, 0, 0, 0],
								"last 10" : [penaltyMinutesNew, 0, 0, 0, 0, 0, 0, 0, 0, 0],
								"total" :penaltyMinutesNew
								}, 
			"ppPoints" : {"last 5" : [ppPointsNew, 0, 0, 0, 0], 
						  "total" : ppPointsNew
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


		# data exists, but update it
		else:

			with open("Player Stats/" + playerName + ".json") as statsFile:
				playerStats = json.load(statsFile)

			gamesPlayedOld = playerStats['gamesPlayed']

			#check if the player file has been changed ie player has played a game
			if (gamesPlayedOld == gamesPlayedNew):
				pass

			else:

				#dict
				goalsOld = playerStats['goals']
				#dict
				assistsOld = playerStats['assists']
				#dict
				pointsOld = playerStats['points']
				#dict
				ppPointsOld = playerStats['ppPoints']
				#dict
				ppGoalsOld = playerStats['ppGoals']
				plusMinusOld = playerStats['plusMinus']
				penaltyMinutesOld = playerStats['penaltyMinutes']

				playerStats['gamesPlayed'] = gamesPlayedNew

				tmp = goalsNew - goalsOld['total']
				playerStats['goals']['last 3'] = [tmp] + goalsOld['last 3'][:2]
				playerStats['goals']['last 5'] = [tmp] + goalsOld['last 5'][:4]
				playerStats['goals']['last 10'] = [tmp] + goalsOld['last 10'][:9]
				playerStats['goals']['total'] = goalsNew

				tmp = assistsNew - assistsOld['total']
				playerStats['assists']['last 3'] = [tmp] + assistsOld['last 3'][:2]
				playerStats['assists']['last 5'] = [tmp] + assistsOld['last 5'][:4]
				playerStats['assists']['last 10'] = [tmp] + assistsOld['last 10'][:9]
				playerStats['assists']['total'] = assistsNew				

				tmp = pointsNew - pointsOld['total']
				playerStats['points']['last 3'] = [tmp] + pointsOld['last 3'][:2]
				playerStats['points']['last 5'] = [tmp] + pointsOld['last 5'][:4]
				playerStats['points']['last 10'] = [tmp] + pointsOld['last 10'][:9]
				playerStats['points']['total'] = pointsNew

				tmp = plusMinusNew - plusMinusOld['total']
				playerStats['plusMinus']['last 3'] = [tmp] + plusMinusOld['last 3'][:2]
				playerStats['plusMinus']['last 5'] = [tmp] + plusMinusOld['last 5'][:4]
				playerStats['plusMinus']['last 10'] = [tmp] + plusMinusOld['last 10'][:9]
				playerStats['plusMinus']['total'] = plusMinusNew				


				tmp = penaltyMinutesNew - penaltyMinutesOld['total']
				playerStats['penaltyMinutes']['last 3'] = [tmp] + penaltyMinutesOld['last 3'][:2]
				playerStats['penaltyMinutes']['last 5'] = [tmp] + penaltyMinutesOld['last 5'][:4]
				playerStats['penaltyMinutes']['last 10'] = [tmp] + penaltyMinutes['last 10'][:9]
				playerStats['penaltyMinutes']['total'] = penaltyMinutesNew			


				tmp = ppPointsNew - ppPointsOld['total']
				playerStats['ppPoints']['last 5'] = [tmp] + ppPointsOld['last 5'][:4]
				playerStats['ppPoints']['total'] = ppPointsNew

				tmp = ppGoalsNew - ppGoalsOld['total']
				playerStats['ppGoals']['last 5'] = [tmp] + ppGoalsOld['last 5'][:4]
				playerStats['ppGoals']['total'] = ppGoalsNew

				playerStats['shGoals'] = shGoalsNew
				playerStats['shots'] = shotsNew

				#rewrite the json file for the player
				with open("Player Stats/" + playerName + ".json", "w") as statsFile:
					json.dump(playerStats, statsFile)
					

	"""This for loop handles the stats for the goalies only"""
	for goalie in goalieData:
		playerName = goalie['playerName']
		gamesPlayedNew = goalie['gamesPlayed']
		playerPositionCode = goalie['playerPositionCode']
		savePctgNew = goalie['savePctg']
		winsNew = goalie['wins']
		shutoutsNew = goalie['shutouts']
		shotsAgainstNew = goalie['shotsAgainst']
		goalsAgainstNew = goalie['goalsAgainst']
		timeOnIceNew = goalie['timeOnIce']
		savesNew = goalie['saves']
		goalsAgainstAverageNew = goalie['goalsAgainstAverage']

		if not os.path.isfile("Player Stats/" + playerName + ".json"):
			outputData = {	
			"playerName": playerName,
			"gamesPlayed" : gamesPlayedNew,
			"playerPositionCode" : playerPositionCode,
			"savePctg" : {"last 3": [savePctgNew, 0, 0],
						"last 5" : [savePctgNew, 0, 0, 0, 0],
						"last 10" : [savePctgNew, 0, 0, 0, 0, 0, 0, 0, 0, 0],
						"total" : savePctgNew
						},
			"wins" : {"last 3" : [winsNew, 0, 0],
						"last 5" : [winsNew, 0, 0, 0, 0],
						"last 10" : [winsNew, 0, 0, 0, 0, 0, 0, 0, 0, 0],
						"total" : winsNew
						},	
			"shutouts" : shutoutsNew,
			"shotsAgainst" : {"last 3" : [shotsAgainstNew, 0, 0],
						"last 5" : [shotsAgainstNew, 0, 0, 0, 0],
						"last 10" : [shotsAgainstNew, 0, 0, 0, 0, 0, 0, 0, 0, 0],
						"total" : shotsAgainstNew
						},
			"goalsAgainst" : {"last 3" : [goalsAgainstNew, 0, 0],
						"last 5" : [goalsAgainstNew, 0, 0, 0, 0],
						"last 10" : [goalsAgainstNew, 0, 0, 0, 0, 0, 0, 0, 0, 0],
						"total" : goalsAgainstNew
						},
			"saves" : {"last 3" : [savesNew, 0, 0],
						"last 5" : [savesNew, 0, 0, 0, 0],
						"last 10" : [savesNew, 0, 0, 0, 0, 0, 0, 0, 0, 0],
						"total" : savesNew
						},
			"goalsAgainstAverage" : {"last 3" : [goalsAgainstAverageNew, 0, 0],
									"last 5" : [goalsAgainstAverageNew, 0, 0, 0, 0],
									"last 10" : [goalsAgainstAverageNew, 0, 0, 0, 0, 0, 0, 0, 0, 0],
									"total" : goalsAgainstAverageNew
						},
			"timeOnIce" : {"last 3" : [timeOnIceNew, 0, 0],
						"last 5" : [timeOnIceNew, 0, 0, 0, 0], 
						"last 10" : [timeOnIceNew, 0, 0, 0, 0, 0, 0, 0, 0, 0],
						"total" : timeOnIceNew
						  }
			}
			with open("Player Stats/" + playerName + ".json", "w") as outfile:
				json.dump(outputData, outfile)						

		else:

			with open("Player Stats/" + playerName + ".json") as statsFile:
				playerStats = json.load(statsFile)

			gamesPlayedOld = playerStats['gamesPlayed']

			if (gamesPlayedOld == gamesPlayedNew):
				pass

			else:
				savePctgOld = playerStats['savePctg']
				winsOld = playerStats['wins']
				shotsAgainstOld = playerStats['shotsAgainst']
				goalsAgainstOld = playerStats['goalsAgainst']
				savesOld = playerStats['saves']
				timeOnIceOld = playerStats['timeOnIce']
				goalsAgainstAverageOld = playerStats['goalsAgainstAverage']

				playerStats['gamesPlayed'] = gamesPlayedNew

				# calculate the SV% of last game; stat in NHL JSON is a cumulative number
				# the shotsAgainst stat counts both saves and goals			
				shotsOnGoalLastGame = shotsAgainstNew - shotsAgainstOld['total']
				savesLastGame = savesNew - savesOld['total']
				tmp = savesLastGame / shotsOnGoalLastGame

				playerStats['savePctg']['last 3'] = [tmp] + savePctgOld['last 3'][:2]
				playerStats['savePctg']['last 5'] = [tmp] + savePctgOld['last 5'][:4]
				playerStats['savePctg']['last 10'] = [tmp] + savePctgOld['last 10'][:9]
				playerStats['savePctg']['total'] = savePctgNew

				tmp = winsNew - winsOld['total']
				playerStats['wins']['last 3'] = [tmp] + winsOld['last 3'][:2]
				playerStats['wins']['last 5'] = [tmp] + winsOld['last 5'][:4]
				playerStats['wins']['last 10'] = [tmp] + winsOld['last 10'][:9]
				playerStats['wins']['total'] = winsNew

				playerStats['shutouts'] = shutoutsNew

				playerStats['shotsAgainst']['last 3'] = [shotsOnGoalLastGame] + shotsAgainstOld['last 3'][:2]
				playerStats['shotsAgainst']['last 5'] = [shotsOnGoalLastGame] + shotsAgainstOld['last 5'][:4]
				playerStats['shotsAgainst']['last 10'] = [shotsOnGoalLastGame] + shotsAgainstOld['last 10'][:9]
				playerStats['shotsAgainst']['total'] = shotsAgainstNew

				goalsAgainstLastGame = goalsAgainstNew - goalsAgainstOld['total']
				playerStats['goalsAgainst']['last 3'] = [goalsAgainstLastGame] + goalsAgainstOld['last 3'][:2]
				playerStats['goalsAgainst']['last 5'] = [goalsAgainstLastGame] + goalsAgainstOld['last 5'][:4]
				playerStats['goalsAgainst']['last 10'] = [goalsAgainstLastGame] + goalsAgainstOld['last 10'][:9]
				playerStats['goalsAgainst']['total'] = goalsAgainstNew

				playerStats['saves']['last 3'] = [savesLastGame] + savesOld['last 3'][:2]
				playerStats['saves']['last 5'] = [savesLastGame] + savesOld['last 5'][:4]
				playerStats['saves']['last 10'] = [savesLastGame] + savesOld['last 10'][:9]
				playerStats['saves']['total'] = savesNew

				timeOnIceLastGame = timeOnIceNew - timeOnIceOld['total']
				playerStats['timeOnIce']['last 3'] = [timeOnIceLastGame] + timeOnIceOld['last 3'][:2]
				playerStats['timeOnIce']['last 5'] = [timeOnIceLastGame] + timeOnIceOld['last 5'][:4]
				playerStats['timeOnIce']['last 10'] = [timeOnIceLastGame] + timeOnIceOld['last 10'][:9]
				playerStats['timeOnIce']['total'] = timeOnIceNew

				goalsAgainstAverageLastGame = goalsAgainstLastGame / timeOnIceLastGame * 60
				playerStats['goalsAgainstAverage']['last 3'] = [goalsAgainstAverageLastGame] + goalsAgainstAverage['last 3'][:2]
				playerStats['goalsAgainstAverage']['last 5'] = [goalsAgainstAverageLastGame] + goalsAgainstAverage['last 5'][:4]
				playerStats['goalsAgainstAverage']['last 10'] = [goalsAgainstAverageLastGame] + goalsAgainstAverage['last 10'][:9]
				playerStats['goalsAgainstAverage']['total'] = goalsAgainstAverageNew

				with open("Player Stats/" + playerName + ".json", "w") as statsFile:
					json.dump(playerStats, statsFile)
					
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

def sortDailyStats():

	#key will be sum of last 3, 5 or 10, values the list of players
	#skater stats will be the sum
	_3Goals = {}
	_5Goals = {}
	_10Goals = {}
	_3Assists = {}
	_5Assists = {}
	_10Assists = {}
	_5Points = {}
	_10Points = {}
	_3Points = {}

	#goalie stats will be average
	_3SavePctg = {}
	_5SavePctg = {}
	_10SavePctg = {}

	_3Wins = {}
	_5Wins = {}
	_10Wins = {}

	_3ShotsAgainst = {}
	_5ShotsAgainst = {}
	_10ShotsAgainst = {}

	_3GoalsAgainst = {}
	_5GoalsAgainst = {}
	_10GoalsAgainst = {}

	_3Saves = {}
	_5Saves = {}
	_10Saves = {}

	_3TimeOnIce = {}
	_5TimeOnIce = {}
	_10TimeOnIce = {}

	_3GAA = {}
	_5GAA = {}
	_10GAA = {}

	if not (os.path.isdir("Daily Reports")):
		os.makedirs("Daily Reports")

	for f in os.listdir("Player Stats"):
		
		with open("Player Stats/" + f) as playerFile:
			data = json.load(playerFile)


		if (data['playerPositionCode'] == 'G'):

			name = data['playerName']

			tmp = statistics.mean(data['savePctg']['last 3'])

			if tmp in _3SavePctg:
				_3SavePctg[tmp].append(name)

			else:
				_3SavePctg[tmp] = [name]

			tmp = statistics.mean(data['savePctg']['last 5'])
			
			if tmp in _5SavePctg:
				_5SavePctg[tmp].append(name)

			else:
				_5SavePctg[tmp] = [name]

			tmp = statistics.mean(data['savePctg']['last 10'])		

			if tmp in _10SavePctg:
				_10SavePctg[tmp].append(name)

			else:
				_10SavePctg[tmp] = [name]


			tmp = statistics.mean(data['wins']['last 3'])

			if tmp in _3Wins:
				_3Wins[tmp].append(name)

			else:
				_3Wins[tmp] = [name]

			tmp = statistics.mean(data['wins']['last 5'])
			
			if tmp in _5Wins:
				_5Wins[tmp].append(name)

			else:
				_5Wins[tmp] = [name]

			tmp = statistics.mean(data['wins']['last 10'])		

			if tmp in _10Wins:
				_10Wins[tmp].append(name)

			else:
				_10Wins[tmp] = [name]


			#shotsAgainst
			tmp = statistics.mean(data['shotsAgainst']['last 3'])

			if tmp in _3ShotsAgainst:
				_3ShotsAgainst[tmp].append(name)

			else:
				_3ShotsAgainst[tmp] = [name]

			tmp = statistics.mean(data['shotsAgainst']['last 5'])
			
			if tmp in _5ShotsAgainst:
				_5ShotsAgainst[tmp].append(name)

			else:
				_5ShotsAgainst[tmp] = [name]

			tmp = statistics.mean(data['shotsAgainst']['last 10'])		

			if tmp in _10ShotsAgainst:
				_10ShotsAgainst[tmp].append(name)

			else:
				_10ShotsAgainst[tmp] = [name]


			#goalsAgainst
			tmp = statistics.mean(data['goalsAgainst']['last 3'])

			if tmp in _3GoalsAgainst:
				_3GoalsAgainst[tmp].append(name)

			else:
				_3GoalsAgainst[tmp] = [name]

			tmp = statistics.mean(data['goalsAgainst']['last 5'])
			
			if tmp in _5GoalsAgainst:
				_5GoalsAgainst[tmp].append(name)

			else:
				_5GoalsAgainst[tmp] = [name]

			tmp = statistics.mean(data['goalsAgainst']['last 10'])		

			if tmp in _10GoalsAgainst:
				_10GoalsAgainst[tmp].append(name)

			else:
				_10GoalsAgainst[tmp] = [name]

			#saves
			tmp = statistics.mean(data['saves']['last 3'])

			if tmp in _3Saves:
				_3Saves[tmp].append(name)

			else:
				_3Saves[tmp] = [name]

			tmp = statistics.mean(data['saves']['last 5'])
			
			if tmp in _5Saves:
				_5Saves[tmp].append(name)

			else:
				_5Saves[tmp] = [name]

			tmp = statistics.mean(data['saves']['last 10'])		

			if tmp in _10Saves:
				_10Saves[tmp].append(name)

			else:
				_10Saves[tmp] = [name]													


			#toi
			tmp = statistics.mean(data['timeOnIce']['last 3'])

			if tmp in _3TimeOnIce:
				_3TimeOnIce[tmp].append(name)

			else:
				_3TimeOnIce[tmp] = [name]

			tmp = statistics.mean(data['timeOnIce']['last 5'])
			
			if tmp in _5TimeOnIce:
				_5TimeOnIce[tmp].append(name)

			else:
				_5TimeOnIce[tmp] = [name]

			tmp = statistics.mean(data['timeOnIce']['last 10'])		

			if tmp in _10TimeOnIce:
				_10TimeOnIce[tmp].append(name)

			else:
				_10TimeOnIce[tmp] = [name]


			#gaa	
			tmp = statistics.mean(data['goalsAgainstAverage']['last 3'])

			if tmp in _3GAA:
				_3GAA[tmp].append(name)

			else:
				_3GAA[tmp] = [name]

			tmp = statistics.mean(data['goalsAgainstAverage']['last 5'])
			
			if tmp in _5GAA:
				_5GAA[tmp].append(name)

			else:
				_5GAA[tmp] = [name]

			tmp = statistics.mean(data['goalsAgainstAverage']['last 10'])		

			if tmp in _10GAA:
				_10GAA[tmp].append(name)

			else:
				_10GAA[tmp] = [name]						

		else:	

			name = data['playerName']

			tmp = sum(data['goals']['last 3'])

			if tmp in _3Goals:
				_3Goals[tmp].append(name)
			else:
				_3Goals[tmp] = [name]

			tmp = sum(data['goals']['last 5'])

			if tmp in _5Goals:
				_5Goals[tmp].append(name)
			else:
				_5Goals[tmp] = [name]

			tmp = sum(data['goals']['last 10'])

			if tmp in _10Goals:
				_10Goals[tmp].append(name)
			else:
				_10Goals[tmp] = [name]

			tmp = sum(data['assists']['last 3'])

			if tmp in _3Assists:
				_3Assists[tmp].append(name)
			else:
				_3Assists[tmp] = [name]

			tmp = sum(data['assists']['last 5'])

			if tmp in _5Assists:
				_5Assists[tmp].append(name)
			else:
				_5Assists[tmp] = [name]

			tmp = sum(data['assists']['last 10'])

			if tmp in _10Assists:
				_10Assists[tmp].append(name)
			else:
				_10Assists[tmp] = [name]

			tmp = sum(data['points']['last 3'])

			if tmp in _3Points:
				_3Points[tmp].append(name)
			else:
				_3Points[tmp] = [name]

			tmp = sum(data['points']['last 5'])

			if tmp in _5Points:
				_5Points[tmp].append(name)
			else:
				_5Points[tmp] = [name]

			tmp = sum(data['points']['last 10'])

			if tmp in _10Points:
				_10Points[tmp].append(name)
			else:
				_10Points[tmp] = [name]


	generateDailySkaterReport(_3Goals, 3, 'goals')
	generateDailySkaterReport(_5Goals, 5, 'goals')
	generateDailySkaterReport(_10Goals, 10, 'goals')
	generateDailySkaterReport(_3Assists, 3, 'assists')
	generateDailySkaterReport(_5Assists, 5, 'assists')
	generateDailySkaterReport(_10Assists, 10, 'assists')
	generateDailySkaterReport(_3Points, 3, 'points')
	generateDailySkaterReport(_5Points, 5, 'points')
	generateDailySkaterReport(_10Points, 10, 'points')

	generateDailyGoalieReport(_3SavePctg, 3, 'savePctg')
	generateDailyGoalieReport(_5SavePctg, 5, 'savePctg')
	generateDailyGoalieReport(_10SavePctg, 10, 'savePctg')

	generateDailyGoalieReport(_3Wins, 3, 'wins')
	generateDailyGoalieReport(_5Wins, 5, 'wins')
	generateDailyGoalieReport(_10Wins, 10, 'wins')


	generateDailyGoalieReport(_3ShotsAgainst, 3, 'shotsAgainst')
	generateDailyGoalieReport(_5ShotsAgainst, 5, 'shotsAgainst')
	generateDailyGoalieReport(_10ShotsAgainst, 10, 'shotsAgainst')


	generateDailyGoalieReport(_3GoalsAgainst, 3, 'goalsAgainst')
	generateDailyGoalieReport(_5GoalsAgainst, 5, 'goalsAgainst')
	generateDailyGoalieReport(_10GoalsAgainst, 10, 'goalsAgainst')	

	generateDailyGoalieReport(_3Saves, 3, 'saves')
	generateDailyGoalieReport(_5Saves, 5, 'saves')
	generateDailyGoalieReport(_10Saves, 10, 'saves')		

	generateDailyGoalieReport(_3TimeOnIce, 3, 'timeOnIce')
	generateDailyGoalieReport(_5TimeOnIce, 5, 'timeOnIce')
	generateDailyGoalieReport(_10TimeOnIce, 10, 'timeOnIce')

	generateDailyGoalieReport(_3GAA, 3, 'goalsAgainstAverage')
	generateDailyGoalieReport(_5GAA, 5, 'goalsAgainstAverage')
	generateDailyGoalieReport(_10GAA, 10, 'goalsAgainstAverage')

	return

def generateDailySkaterReport(dictionary, lastXGames, stat):

	keys = list(dictionary.keys())

	keys.sort(reverse=True)

	n = "Name"
	t = "Total"

	today = datetime.date.today().isoformat()

	if not (os.path.isdir("Daily Reports/" + today)):
		os.makedirs("Daily Reports/" + today)	

	fileName = today + " Last " + str(lastXGames) + " " + stat

	last = "Last " + str(lastXGames) + " Games"
	header = [n, t, last]
	with open("Daily Reports/" + today + "/" + fileName + ".csv", "w", newline='') as outfile:
		w = csv.writer(outfile)

		w.writerow(header)

		for key in keys:
			for name in dictionary[key]:

				with open("Player Stats/" + name + ".json") as f:
					data = json.load(f)

				lastNGames = str(data[stat]['last ' + str(lastXGames)])
				iterable = [name, key, lastNGames.strip("[]")]

				w.writerow(iterable)

	return

def generateDailyGoalieReport(dictionary, lastXGames, stat):

	keys = list(dictionary.keys())

	if stat == 'goalsAgainst' or stat == 'goalsAgainstAverage':
		keys.sort()

	else:
		keys.sort(reverse = True)


	today = datetime.date.today().isoformat()

	if not (os.path.isdir("Daily Reports/" + today)):
		os.makedirs("Daily Reports/" + today)


	fileName = today + " Last " + str(lastXGames) + " " + stat

	last = "Last " + str(lastXGames) + " Games"

	header = ['Name', 'Season Total', 'Avg Over ' + str(lastXGames) + ' Games' , last]

	with open("Daily Reports/" + today + "/" + fileName + ".csv", "w", newline='') as outfile:
		w = csv.writer(outfile)

		w.writerow(header)

		for key in keys:
			for name in dictionary[key]:

				with open("Player Stats/" + name + ".json") as f:
					data = json.load(f)

				lastNGames = str(data[stat]['last ' + str(lastXGames)])
				iterable = [name, data[stat]['total'], key, lastNGames.strip("[]")]

				w.writerow(iterable)	








updateDatabase()
sortDailyStats()