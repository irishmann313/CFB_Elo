from bs4 import BeautifulSoup
import requests
import re

for i in range(1992, 2018):
    requesturl = "https://www.sports-reference.com/cfb/years/"+str(i)+"-schedule.html"
    r = requests.get(requesturl)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    games = ''

    currentweek = 1

    #find week number and team names
    for line in soup.find_all('td'):
	if 'week_number' in str(line): 
	    week = re.sub(r'\D', "", str(line))
            week = week[:2]
	    week = week.lstrip("0")
	    if currentweek != int(week):
		games += '\n'
		currentweek += 1
	if 'winner_school_name' in str(line):
	    winner_start_index = str(line).find('html">')
	    winner_end_index = str(line).find("</a>")
	    if winner_start_index == -1:
		winner_start_index = str(line).find('name">')
		winner_end_index = str(line).find('</td>')
	    wfix = str(line)[winner_start_index+6:winner_end_index]
	    wfix = wfix.replace("&amp;", "&")
	    winner = wfix
	    games += (winner + ',')
	if 'loser_school_name' in str(line):
	    loser_start_index = str(line).find('html">')
	    loser_end_index = str(line).find("</a>")
	    if loser_start_index == -1:
		loser_start_index = str(line).find('name">')
		loser_end_index = str(line).find('</td>')
	    lfix = str(line)[loser_start_index+6:loser_end_index]
	    lfix = lfix.replace("&amp;", "&")
	    loser = lfix
	    games += (loser + ',' + winner + '::')

    outputfile = 'schedule_' + str(i) + '.txt'
    file = open(outputfile, 'w')
    file.write(games)
    file.close()
