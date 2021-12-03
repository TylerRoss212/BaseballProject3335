from flask import Flask, render_template, request
import pymysql
import hashlib

app = Flask(__name__)
con = pymysql.connect(host='localhost', user='root', password='', database='GiveUsAnADrSpeegle')
cur = con.cursor()

@app.route('/')
def form():
    return render_template('home.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signupSuccess', methods=['POST', 'GET'])
def signupSuccess():
    if request.method == 'POST':
        form_data = request.form

        params = []
        params.append(form_data['username'])
        params.append(hashlib.sha256(form_data['password'].encode('utf-8')).hexdigest())

        try:
            sql = 'INSERT INTO Users (username, password) VALUES (%s, %s)'
            print(sql)
            cur.execute(sql, params)

        except Exception:
            con.rollback()
            print("Database Exception")
            raise
        else:
            con.commit()
        finally:
            con.close()

        return render_template('signupSuccess.html')

@app.route('/login')
def login():
    return render_template('login.html')

        
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':

        form_data = request.form

        params = []
        params.append(form_data['username'])

        try:
            sql = "SELECT password FROM Users WHERE username = %s"
            print(sql)
            cur.execute(sql, params)

            results = cur.fetchall()
            passMatch = hashlib.sha256(form_data['password'].encode('utf-8')).hexdigest()

            for row in results:
                if(row == passMatch):
                    return render_template('dashboard.html', form_data=form_data)
                else:
                    alert("BAD")


        except Exception:
            con.rollback()
            print("Database Exception")
            raise
        else:
            con.commit()
        finally:
            con.close()
