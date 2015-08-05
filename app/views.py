from flask import render_template
from app import app
from app import api
from app.matrix import redis

def render_journey(jid):
    a, b = jid.split("/")
    afull = redis.get(a)
    bfull = redis.get(b)
    count = redis.scard(jid)
    return {"start": a, "end": b, "start_full": afull, "end_full": bfull, "count": count}

@app.route('/')
def index():
    keys = redis.smembers("allkeys")
    stations = [{"sid":key, "fullname":redis.get(key)} for key in keys]
    stations = sorted(stations, key = lambda x:x["fullname"])
    return render_template('index.html', stations=stations)


@app.route('/view/<station_id>')
def station_view(station_id):
    # TODO: this data should come from an api call tbh
    sid = station_id.lower()
    fullname = redis.get(sid)
    keys = redis.keys(sid + "/*")
    journeys = [render_journey(key) for key in keys]
    return render_template('station.html', journeys=journeys, fullname=fullname)

@app.route('/view/<a>/<b>')
def journey_view(a, b):
    # TODO: this data should come from an api call tbh
    sida = a.lower()
    sidb = b.lower()
    fullnamea = redis.get(sida)
    fullnameb = redis.get(sidb)
    count = redis.scard("{:}/{:}".format(sida, sidb))
    return render_template('journey.html', fullnamea=fullnamea, fullnameb=fullnameb, count=count)
