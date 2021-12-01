from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

@app.route('/signup')
def form():
    return render_template('signup.html')
        
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        form_data = request.form
        print(hashlib.sha256(form_data['password'].encode('utf-8')).hexdigest())
        return render_template('dashboard.html', form_data=form_data)