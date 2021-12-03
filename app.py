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

@app.route('/changeFav', methods=['POST'])
def changeFav():
    if request.method == 'POST':
        form_data = request.form
        changeParam = []
        print('1')
        changeParam.append(form_data['teams'])
        print('2')
        changeParam.append(form_data['username'])
        print('3')
        print(changeParam[0])
        print(changeParam[1])
        sql = 'UPDATE Users SET favoriteTeam = %s WHERE username = %s'
        print(sql)
        cur.execute(sql, changeParam)

        username = form_data['username']
        return render_template('changeFav.html')
        
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():

    if request.method == 'POST':

        sql = 'SELECT name, teamid FROM teams WHERE year=2020'
        print(sql)
        cur.execute(sql)

        teams = cur.fetchall()
        teamsList = []

        for row in teams:
            teamsList.append(row)


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



            sql = "SELECT year FROM Teams GROUP BY year"
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
                        return render_template('dashboard.html', username=username, teams=teamsList, years=yearList, favTeam=favTeam)
                    else:
                        return render_template('incorrectUserOrPass.html')


        except Exception:
            con.rollback()
            print("Database Exception")
            raise
        else:
            con.commit()
