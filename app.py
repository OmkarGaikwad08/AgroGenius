
# DUE TO COPYRIGHT ISSUE THE ORIGINAL CODE IS NOT UPLOADED YOU CAN USE THIS CODE FOR REFERENCE PURPOSE


from flask import Flask, render_template, request, redirect, url_for, session
from tinydb import TinyDB, Query
import hashlib
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import requests
import json
import joblib
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Sample database setup (not functional)
db = TinyDB('database_sample.json')
users_table = db.table('users')

weather_db = TinyDB('weather_database_sample.json')
weather_table = weather_db.table('weather')

npk_db = TinyDB('npk_database_sample.json')
npk_table = npk_db.table('npk')

st_db = TinyDB('st_database_sample.json')
st_table = st_db.table('st')

# Sample crop dataset
crop_data = pd.DataFrame({
    'nitrogen': [10, 20, 30],
    'phosphorus': [15, 25, 35],
    'potassium': [5, 10, 15],
    'label': ['Crop A', 'Crop B', 'Crop C']
})

# Sample ST data
st_data = pd.DataFrame({
    'soilType': ['Loamy', 'Sandy', 'Clay']
})

def get_weather_data(city):
    # Sample weather data
    return {
        'temperature': '25',
        'weather_description': 'Clear sky',
        'humidity': '60',
        'wind_speed': '5'
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        users_table.insert({'username': username, 'password': hashed_password})
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        User = Query()
        user = users_table.get(User.username == username)
        if user and user['password'] == hashed_password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error=True)
    return render_template('login.html', error=False)

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        # Sample model prediction
        if True:  # Replace with actual model prediction logic
            user_input = [10, 20, 30, 25, 60]
            crop = 'Sample Crop'  # Placeholder prediction
            return render_template('dashboard.html', username=session['username'], crop=crop)
        else:
            return render_template('dashboard.html', username=session['username'])
    
    return redirect(url_for('index'))

@app.route('/dashboard1')
def dashboard1():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/weather', methods=['GET','POST'])
def weather():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            city = request.form['city']
            weather_data = get_weather_data(city)
            return render_template('weather.html', city=city, **weather_data, username=username)
        else:
            return render_template('weather.html', city='', temperature='', weather_description='', humidity='', wind_speed='', username=username)

@app.route('/npk')
def npk():
    if 'username' in session:
        return render_template('npk.html')
    else:
        return redirect(url_for('index'))

@app.route('/stok', methods=['POST'])
def st():
    soilType = request.form['soilType']
    st_table.truncate()
    st_table.insert({'soilType':soilType})
    return redirect(url_for('dashboard1'))

@app.route('/npks', methods=['POST'])
def npks():
    nitrogen = request.form['nitrogen']
    phosphorus = request.form['phosphorus']
    potassium = request.form['potassium']
    npk_table.truncate()
    npk_table.insert({'nitrogen': nitrogen, 'phosphorus': phosphorus, 'potassium': potassium})
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
