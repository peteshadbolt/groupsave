from flask import render_template
from gs import app
import api, redis
import time

@app.route('/')
def index():
    output = render_template('index.html')
    return output

@app.route('/view/<crs1>/<crs2>/<when>')
def journey_view(crs1, crs2, when):
    data = api.JourneyItem().get(crs1, crs2, when)
    return render_template('journey.html', data=data)
