import sys
import math
import os

def open_team_file():
	team_file = open('teams.txt','r')
	teams = team_file.readlines()
	team_file.close()
	return teams

def rewrite_team_file(elos):
	team_file = open('teams_2000.txt', 'w')
	for team in elos:
		team_file.write(team['name'] + "::" + str(team['elo']) + '\n')
	team_file.close()

if __name__ == '__main__':
	#setup list of dicts
	teams = open_team_file()
	elos = []
	for team in teams:
		split = team.split("::")
		teamelo = {'name':split[0], 'elo':float(split[1].rstrip())}
		elos.append(teamelo)

	#run through the season
	schedule_file = open('schedule_2000.txt', 'r')
	weeks = schedule_file.readlines()
	schedule_file.close()
	totalgames = 0
	totalcorect = 0
        for week in weeks:
	        games = week.split("::")
		for game in games:
			totalgames += 1
			if game == '\n' or game == '': 
				continue
			split = game.split(",")
			team1 = split[0]
			team2 = split[1]
			winner = split[2]

			team1_dict = {}
			team2_dict = {}
			for item in elos: 
				if item['name']==team1:
					team1_dict = item
				if item['name']==team2:
					team2_dict = item
			if not team1_dict:
				team1_dict['name'] = team1
				team1_dict['elo'] = 1500
			if not team2_dict:
				team2_dict['name'] = team2
				team2_dict['elo'] = 1500

			if team1_dict['elo'] > team2_dict['elo']:
				predictedwinner = team1
			elif team2_dict['elo'] > team1_dict['elo']:
				predictedwinner = team2
			else:
				predictedwinner = "tie"

			if predictedwinner == winner:
				totalcorect += 1

			R1 = int(team1_dict['elo'])
			R2 = int(team2_dict['elo'])
			Q1 = math.pow(10, (R1/400))
			Q2 = math.pow(10, (R2/400))
			E1 = Q1/(Q1+Q2)
			E2 = Q2/(Q1+Q2)

			if winner==team1_dict['name']:
				if R1<2100:
					k=32
				elif R1>=2100 and R1<=2400:
					k=24
				else:
					k=16
				R1 = R1 + k*(1-E1)
				R2 = R2 + k*(0-E2)
			else:
				if R2<2100:
					k=32
				elif R2>=2100 and R2<=2400:
					k=24
				else:
					k=16
				R1 = R1 + k*(0-E1)
				R2 = R2 + k*(1-E1)

			for team in elos:
				if team['name']==team1:
					team['elo'] = R1
				if team['name']==team2:
					team['elo'] = R2

        accuracy = totalcorect/totalgames
	file = open('accuracy.txt', 'a')
	file.write(str(accuracy)+'\n')
	file.close()	

	# write back to the teams file
	rewrite_team_file(elos)
