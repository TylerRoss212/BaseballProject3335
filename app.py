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

            #Establish login for dashboard
            sql = "SELECT password FROM Users WHERE username = %s"
            print(sql)
            cur.execute(sql, params)
            results = cur.fetchall()

            #Reder dashboard if valid login and show incorrect otherwise
            for row in results:
                for col in row:
                    if(col == passMatch):
                        return render_template('dashboard.html', username=username, teams=teamsList, years=yearList, favTeam=favTeam, favTeamName=favTeamName, password=password)
                    else:
                        return render_template('incorrectUserOrPass.html')


        except Exception:
            con.rollback()
            print("Database Exception")
            raise
        else:
            con.commit()

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