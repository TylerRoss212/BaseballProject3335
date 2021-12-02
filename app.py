from flask import Flask, render_template, request
import pymysql
import hashlib

app = Flask(__name__)
con = pymysql.connect(host='localhost', user='root', password='', database='GiveUsAnADrSpeegle')
cur = con.cursor()

@app.route('/')
def form():
    return render_template('signup.html')
        
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        form_data = request.form
        #print(hashlib.sha256(form_data['password'].encode('utf-8')).hexdigest())

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

        return render_template('dashboard.html', form_data=form_data)
