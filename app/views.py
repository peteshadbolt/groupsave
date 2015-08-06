from flask import render_template
from app import app
from app import api
from app.api import StationItem
from app.api import JourneyItem
from app.matrix import redis

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/view/<crs>')
def station_view(crs):
    # TODO: this data should come from an api call tbh
    data = StationItem.get(crs)
    return render_template('station.html', data=data)

@app.route('/view/<crs1>/<crs2>')
def journey_view(crs1, crs2):
    data = JourneyItem.get(crs1, crs2)
    return render_template('journey.html', data=data)
