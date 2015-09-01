from flask import render_template
from app import app, api, redis

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view/<crs1>/<crs2>/<when>')
def journey_view(crs1, crs2, when):
    data = api.JourneyItem().get(crs1, crs2, when)
    return render_template('journey.html', data=data)
