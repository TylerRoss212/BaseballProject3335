from flask import Flask, render_template, request
import pymysql
import hashlib
import json

app = Flask(__name__)
con = pymysql.connect(host='localhost', user='root', password='', database='GiveUsAnADrSpeegle')
cur = con.cursor()

#Home page render
@app.route('/')
def form():
    return render_template('home.html')

#Sign up render
@app.route('/signup')
def signup():
    try:
        #SQL to get the teams list to choose favorite team
        sql = 'SELECT name, teamid FROM teams WHERE year=2020'
        print(sql)
        cur.execute(sql)
    
    except Exception:
        con.rollback()
        print('Error: unable to fetch data')
        raise

    else:
        con.commit()

    #Fetch teams list for the signup
    teams = cur.fetchall()
    teamsList = []
    
    for row in teams:
        teamsList.append(row)

    return render_template('signup.html', teams=teamsList)

#Sign up success render
@app.route('/signupSuccess', methods=['POST', 'GET'])
def signupSuccess():
    if request.method == 'POST':
        form_data = request.form

        #Load parameters for user insert
        params = []
        params.append(form_data['username'])
        params.append(hashlib.sha256(form_data['password'].encode('utf-8')).hexdigest())
        params.append(form_data['teams'])

        try:
            #Insert new user into table
            sql = 'INSERT INTO Users VALUES (%s, %s, %s)'
            print(sql)
            cur.execute(sql, params)

        except Exception:
            con.rollback()
            print("Database Exception")
            raise
        else:
            con.commit()

        return render_template('signupSuccess.html')

#Login render
@app.route('/login')
def login():
    return render_template('login.html')

#Change favorite team render
@app.route('/changeFav', methods=['POST'])
def changeFav():
    if request.method == 'POST':

        form_data = request.form

        #Load parameters for favorite team alter
        changeParam = []
        changeParam.append(form_data['teams'])
        changeParam.append(form_data['username'])

        try:
            #Update users favorite team based on submission
            sql = 'UPDATE Users SET favoriteTeam = %s WHERE username = %s'
            print(sql)
            cur.execute(sql, changeParam)

        except Exception:
            con.rollback()
            print("Database Exception")
            raise
        else:
            con.commit()

        #Reestablish login
        username = form_data['username']
        password = form_data['password']

        return render_template('changeFav.html', username=username, password=password)

#Dashboard render
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():

    if request.method == 'POST':

        form_data = request.form

        #Establish login
        username = form_data['username']
        password = form_data['password']
        passMatch = hashlib.sha256(form_data['password'].encode('utf-8')).hexdigest()

        #Reestablish teams list
        sql = 'SELECT name, teamid FROM teams WHERE year=2020'
        print(sql)
        cur.execute(sql)
        teams = cur.fetchall()
        teamsList = []
        for row in teams:
            teamsList.append(row)

        #Initialize parameters for favorite team fetch and years
        params = []
        tempNameParam = []
        yearList = []
        params.append(username)

        try:

            #Establish login for dashboard
            sql = "SELECT password FROM Users WHERE username = %s"
            print(sql)
            cur.execute(sql, params)
            results = cur.fetchall()

            #Reder dashboard if valid login and show incorrect otherwise
            for row in results:
                for col in row:
                    if(col == passMatch):

                        #Find favorite team
                        sql = "SELECT favoriteTeam FROM Users WHERE username = %s"
                        cur.execute(sql, params)
                        favSQL = cur.fetchall()

                        for team in favSQL:
                            favTeam = (team[0])


                        #Based on teamID, find teamName
                        tempNameParam.append(favTeam)
                        sql = "SELECT name FROM Teams WHERE teamID = %s GROUP BY name"
                        cur.execute(sql, tempNameParam)
                        tempNameSQL = cur.fetchall()

                        for team in tempNameSQL:
                            favTeamName = (team[0])


                        #Reestablish years list
                        sql = "SELECT year FROM Teams GROUP BY year DESC"
                        cur.execute(sql)
                        allYears = cur.fetchall()

                        for year in allYears:
                                yearList.append(year[0])

                        return render_template('dashboard.html', username=username, teams=teamsList, years=yearList, favTeam=favTeam, favTeamName=favTeamName, password=password)


        except Exception:
            con.rollback()
            print("Database Exception")
            raise
        else:
            con.commit()

        return render_template('incorrectUserOrPass.html')


#cheater standings
@app.route('/cheaters', methods=['POST'])
def cheaters():
    if request.method == 'POST':

        sql = "SELECT t.name, t.year, c.description FROM CaughtCheating c NATURAL JOIN Teams t"
        cur.execute(sql)
        res = cur.fetchall()

        cheatersList = []

        for thing in res:
            cheatersList.append(thing)

        return render_template('cheaters.html', cheatersList=cheatersList)

#Roster standings
@app.route('/standing', methods=['POST'])
def standing():

    if request.method == 'POST':

        form_data = request.form

        #Fetch data from forms
        year = form_data['years']

        params = []
        params.append(year)

        try:
            #Execute roster fetch based on year and fav team
            if(int(year) > 1968):
                sql = "select teamid, name, lgId, divId, W, L from teams where year = %s and divWin = 'Y'"
            else:
                sql = "select teamid, name, lgId, divId, W, L from teams where year = %s and lgWin = 'Y'"


            cur.execute(sql, params)

        except Exception:
            con.rollback()
            print("Database Exception")
            raise

        else:
            con.commit()

        #load results for render
        res = cur.fetchall()
        divWinners = []
        for row in res:
            myStr = ""
            for col in row:
                myStr += str(col)
                myStr += ' '

            divWinners.append((row[0], row[2], row[3], row[4], row[5]))


        searchList = []
        tables = []
        headers = []
        num = 0

        for winner in divWinners:

            num += 1

            subList = []

            if(int(year) > 1968):
                divSql = "select name, G, Ghome, W, L, attendance, (((%s - W) + (L - %s)) / 2) as GB from teams where year = %s and lgID = %s and divId = %s ORDER BY GB ASC;"

                params = []
                params.append(winner[3])
                params.append(winner[4])
                params.append(year)
                params.append(winner[1])
                params.append(winner[2])

                cur.execute(divSql, params)
                res = cur.fetchall()
                headers.append(year + " " + winner[1] + " " + winner[2] + " Standings" + "\n")

            else:
                divSql = "select name, G, Ghome, W, L, attendance, (((%s - W) + (L - %s)) / 2) as GB from teams where year = %s and lgID = %s ORDER BY GB ASC;"

                params = []
                params.append(winner[3])
                params.append(winner[4])
                params.append(year)
                params.append(winner[1])

                cur.execute(divSql, params)
                res = cur.fetchall()
                headers.append(year + " " + winner[1] + " " + " Standings" + "\n")



            for row in res:
                subList.append(row)

            tables.append(subList)

        lgWinnerParams = []
        lgWinnerParams.append(year)
        sql = "SELECT name, lgID FROM Teams WHERE lgWin='Y' AND year = %s"
        cur.execute(sql, lgWinnerParams)
        lgWinRes = cur.fetchall()

        lgWinners = []

        for thing in lgWinRes:
            lgWinners.append(thing)

        wsResults = []

        if(int(year) >= 1903 and int(year) != 1904 and int(year) != 1994):
            wsWinnerParams = []
            wsWinnerParams.append(year)
            sql = "SELECT winner, loser, series FROM WorldSeries WHERE year = %s"
            cur.execute(sql, wsWinnerParams)
            wsWinRes = cur.fetchall()

            for thing in wsWinRes:
                winner = thing[0]
                loser = thing[1]
                series = thing[2]

            #Based on winner ID, find teamName
            tempNameParam = []
            tempNameParam.append(winner)
            sql = "SELECT name FROM Teams WHERE teamID = %s GROUP BY name"
            cur.execute(sql, tempNameParam)
            tempNameSQL = cur.fetchall()

            for team in tempNameSQL:
                winner = (team[0])

            #Based on loser ID, find teamName
            tempNameParam = []
            tempNameParam.append(loser)
            sql = "SELECT name FROM Teams WHERE teamID = %s GROUP BY name"
            cur.execute(sql, tempNameParam)
            tempNameSQL = cur.fetchall()

            for team in tempNameSQL:
                loser = (team[0])

            wsResults.append(winner)
            wsResults.append(loser)
            wsResults.append(series)

        return render_template('standing.html', year=year, tables=tables, headers=headers, num=num, lgWinners=lgWinners, wsResults=wsResults)

#Roster render
@app.route('/roster', methods=['POST']) 
def roster():
    if request.method == 'POST':
        form_data = request.form

        #Fetch data from forms
        year = form_data['years']
        favTeam = form_data['favTeam']

        #Establish parameters list for table load
        params = []
        params.append(year)
        params.append(favTeam)

        try:
            #Execute roster fetch based on year and fav team
            sql = "SELECT CONCAT(nameFirst, ' ', nameLast) as name, CONCAT(birthCountry, ', ', birthState, ', ', birthCity) as birthPlace, CASE WHEN bs.AB IS NULL THEN 'N' WHEN bs.AB = 0 THEN 'N' ELSE 'Y' END as batting, CASE WHEN ps.G IS NULL THEN 'N' WHEN ps.G = 0 THEN 'N' ELSE 'Y' END as pitching, CASE WHEN COALESCE(EXTRACT(MONTH FROM deathDate), EXTRACT(MONTH FROM now())) - EXTRACT(MONTH FROM birthDate) < 0 THEN COALESCE(EXTRACT(YEAR FROM deathDate), EXTRACT(YEAR FROM now())) - EXTRACT(YEAR FROM birthDate) - 1 WHEN COALESCE(EXTRACT(MONTH FROM deathDate), EXTRACT(MONTH FROM now())) - EXTRACT(MONTH FROM birthDate) > 0 THEN COALESCE(EXTRACT(YEAR FROM deathDate), EXTRACT(YEAR FROM now())) - EXTRACT(YEAR FROM birthDate) ELSE CASE WHEN COALESCE(EXTRACT(DAY FROM deathDate), EXTRACT(DAY FROM now())) - EXTRACT(DAY FROM birthDate) >= 0 THEN COALESCE(EXTRACT(YEAR FROM deathDate), EXTRACT(YEAR FROM now())) - EXTRACT(YEAR FROM birthDate) ELSE COALESCE(EXTRACT(YEAR FROM deathDate), EXTRACT(YEAR FROM now())) - EXTRACT(YEAR FROM birthDate) - 1 END END AS Age FROM players p JOIN people USING (personid) LEFT JOIN battingstats bs USING (battingID) LEFT JOIN pitchingstats ps USING (pitchingID) WHERE p.year=%s AND p.teamid=%s"
            cur.execute(sql, params)

        except Exception:
            con.rollback()
            print("Database Exception")
            raise

        else:
            con.commit()

        #load results for render
        results = cur.fetchall()
        rosterList = []
        for row in results:
            rosterList.append(row)

        return render_template('roster.html', year=year, favTeam=favTeam, rosterList=rosterList)

@app.route('/searchBatters', methods=['POST'])
def searchBatters():
    if request.method == 'POST':
        form_data = request.form

        search = form_data['search']
        search = "%" + search + "%"

        #sql statement for the search
        try:
            sql = "SELECT CONCAT(nameFirst, ' ', nameLast), G, AB, R, H, twoB, threeB, HR, RBI, SB, CS, BB, SO, IBB, HBP, SH, SF, GIDP, year FROM people JOIN players USING(personID) JOIN battingstats USING(battingID) WHERE CONCAT(nameFirst, ' ', nameLast) LIKE %s"
            print(sql)
            cur.execute(sql, search)
        
        except Exception:
            con.rollback()
            print("Database Exception")
            raise

        else:
            con.commit()

        #load results for render
        results = cur.fetchall()

        searchList = []
        for row in results:
            searchList.append(row)

        #change search back to normal
        search = search.replace("%", "")

        return render_template('searchBatters.html', search=search, searchList=searchList)

@app.route('/searchPitchers', methods=['POST'])
def searchPitchers():
    if request.method == 'POST':
        form_data = request.form

        search = form_data['search']
        search = "%" + search + "%"

        #sql statement for the search
        try:
            sql = "SELECT CONCAT(nameFirst, ' ', nameLast), W, L, G, GS, CG, SHO, SV, IPouts, H, ER, HR, BB, SO, BAOpp, ERA, IBB, WP, HBP, BK, BFP, GF, R, SH, SF, GIDP, year FROM people JOIN players USING(personID) JOIN pitchingstats USING(pitchingID) WHERE CONCAT(nameFirst, ' ', nameLast) LIKE %s"
            print(sql)
            cur.execute(sql, search)
        
        except Exception:
            con.rollback()
            print("Database Exception")
            raise

        else:
            con.commit()

        #load results for render
        results = cur.fetchall()

        searchList = []
        for row in results:
            searchList.append(row)

        #change search back to normal
        search = search.replace("%", "")

        return render_template('searchPitchers.html', search=search, searchList=searchList)