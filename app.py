from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/signup')
def form():
    return render_template('signup.html')
        
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        form_data = request.form
        return render_template('dashboard.html', form_data=form_data)