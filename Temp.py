import pymysql
import sys

params = []
params.append(sys.argv[1])

con = pymysql.connect(host='localhost', user='root', password='', database='GiveUsAnADrSpeegle')
cur = con.cursor()

divLeadsSql = "select teamid, name, lgId, divId, W, L from teams where year = %s and divWin = 'Y';"
cur.execute(divLeadsSql, params)

res = cur.fetchall()
divWinners = []

for row in res:
    myStr = ""
    for col in row:
        myStr += str(col)
        myStr += ' '

    divWinners.append((row[0], row[2], row[3], row[4], row[5]))
    #print(myStr)


for winner in divWinners:
    divSql = "select name, G, Ghome, W, L, attendance, (((%s - W) + (L - %s)) / 2) as GB from teams where year = %s and lgID = %s and divId = %s ORDER BY GB ASC;"
    params = []
    params.append(winner[3])
    params.append(winner[4])
    params.append(sys.argv[1])
    params.append(winner[1])
    params.append(winner[2])

    cur.execute(divSql, params)
    res = cur.fetchall()
    print(sys.argv[1], " ", winner[1], " ", winner[2], " Standings")

    for row in res:
        myStr = ""
        for col in row:
            myStr += str(col)
            myStr += ' '
        print(myStr)

    print()
