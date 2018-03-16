# New main script to generate yearly Elo rating

import json

if __name__ == '__main__':
    teams = json.load(open('teams.json'))

    # run through the seasons
    for year in range(1992, 2018):
        schedule_file = 'schedule_'+str(year)+'.txt'
        schedule = open(schedule_file, 'r')
        weeks = schedule.readlines()
        schedule.close()
        totalgames=0
        totalcorrect=0
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

            if teams[team1]:
                team1_elo = teams[team1][year]
            else:
                team1_elo = 1500
            if teams[team2]:
                team2_elo = teams[team2][year]
            else:
                team2_elo = 1500

            if team1_elo > team2_elo:
                predictedwinner = team1
            elif team2_elo > team1_elo:
                predictedwinner = team2
            else:
                predictedwinner = "tie"

            if predictedwinner == winner:
                totalcorrect += 1

            R1 = int(team1_elo)
            R2 = int(team2_elo)
            Q1 = math.pow(10, (R1/400))
            Q2 = math.pow(10, (R2/400))
            E1 = Q1/(Q1+Q2)
            E2 = Q2/(Q1+Q2)

            if winner == team1:
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
                R2 = R2 + k*(1-E2)
                R1 = R1 + k*(0-E1)
            teams[team1][year] = R1
            teams[team2][year] = R2
        accuracy = totalcorrect/totalgames
        file = open('accuracy.txt', 'a')
        entry = (year+": "+str(accuracy)+'\n')
        file.write(entry)
        file.close()

        with open('teams.json', 'w') as outfile:
            json.dump(teams, outfile)
