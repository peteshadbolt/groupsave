from flask import render_template
from app import app

@app.route('/')
def index():
    stuff = {'foo': 'bar'}  
    return render_template('index.html', stuff=stuff)
