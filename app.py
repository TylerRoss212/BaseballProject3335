from flask import Flask, render_template, request
import pymysql
import hashlib
import json

app = Flask(__name__)
con = pymysql.connect(host='localhost', user='root', password='', database='GiveUsAnADrSpeegle')
cur = con.cursor()

@app.route('/')
def form():
    return render_template('home.html')

@app.route('/signup')
def signup():
    try:
        sql = 'SELECT name, teamid FROM teams WHERE year=2020'
        print(sql)
        cur.execute(sql)
    
    except Exception:
        con.rollback()
        print('Error: unable to fetch data')
        raise

    else:
        con.commit()

    teams = cur.fetchall()
    teamsList = []
    
    for row in teams:
        teamsList.append(row)

    return render_template('signup.html', teams=teamsList)

@app.route('/signupSuccess', methods=['POST', 'GET'])
def signupSuccess():
    if request.method == 'POST':
        form_data = request.form

        params = []
        params.append(form_data['username'])
        params.append(hashlib.sha256(form_data['password'].encode('utf-8')).hexdigest())
        params.append(form_data['teams'])

        try:
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

@app.route('/login')
def login():
    return render_template('login.html')

        
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':

        form_data = request.form

        username = form_data['username']

        params = []
        params.append(username)

        try:

            sql = "SELECT favoriteTeam FROM Users WHERE username = %s"
            cur.execute(sql, params)
            favSQL = cur.fetchall()

            for team in favSQL:
                    favTeam = (team[0])



            sql = "SELECT year FROM Teams GROUP BY year DESC"
            cur.execute(sql)
            allYears = cur.fetchall()

            yearList = []

            for year in allYears:
                    yearList.append(year[0])

            sql = "SELECT password FROM Users WHERE username = %s"
            print(sql)
            cur.execute(sql, params)

            results = cur.fetchall()
            passMatch = hashlib.sha256(form_data['password'].encode('utf-8')).hexdigest()

            for row in results:
                for col in row:
                    if(col == passMatch):
                        return render_template('dashboard.html', username=username, years=yearList, favTeam=favTeam)
                    else:
                        return render_template('incorrectUserOrPass.html')


        except Exception:
            con.rollback()
            print("Database Exception")
            raise
        else:
            con.commit()

@app.route('/roster', methods=['POST']) 
def roster():
    if request.method == 'POST':
        form_data = request.form

        year = form_data['years']
        favTeam = form_data['favTeam']

        params = []
        params.append(year)
        params.append(favTeam)

        try:
            sql = 'SELECT name, birthCountry FROM players JOIN people USING (personid) WHERE year=%s AND teamid=%s'
            print(sql)
            cur.execute(sql, params)

        except Exception:
            con.rollback()
            print("Database Exception")
            raise

        else:
            con.commit()

        results = cur.fetchall()
        rosterList = []
        for row in results:
            rosterList.append(row)

        return render_template('roster.html', year=year, favTeam=favTeam, roster=rosterList)