import pymysql
con = pymysql.connect(host='localhost', user='root', password='', database='GiveUsAnADrSpeegle')
cur = con.cursor()

f1 = open("./myFile.csv", "r")
next(f1)

f2 = open("./baseballdatabank/core/WorldSeries.csv", "w")

for line in f1:
    readData = line.split(",")
    writeData = []
    winTeam = readData[1]
    loseTeam = readData[2]
    writeData.append(readData[0])

    sql = "SELECT teamID FROM Teams WHERE name = %s GROUP BY teamID LIMIT 1;"
    cur.execute(sql, winTeam)
    res = cur.fetchone()[0]
    writeData.append(res)


    sql = "SELECT teamID FROM Teams WHERE name = %s GROUP BY teamID LIMIT 1;"
    cur.execute(sql, loseTeam)
    res = cur.fetchone()[0]
    writeData.append(res)

    writeData.append(readData[3])

    writeStr = ",".join(writeData)
    f2.write(writeStr)

con.close()



