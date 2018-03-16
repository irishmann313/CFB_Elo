import json
from pprint import pprint

teamsfile = open('teams.txt', 'r')
teams = teamsfile.readlines()
teamslist = []
for team in teams:
    split = team.split("::")
    teamslist.append(split[0])
teams_dict = {}
for team in teamslist:
    teams_dict[team] = {}
    teams_dict[team]['1992'] = 1500
teams_json = json.dumps(teams_dict, indent=4, sort_keys=True)
outfile = open('teams.json', 'w')
outfile.write(teams_json)
outfile.close()
