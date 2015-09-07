#!/usr/bin/python
from flask import Flask, request, jsonify, render_template, redirect
from redis import StrictRedis
from stations import stations, stations_clean, fuzzy_match
import arrow
import re
import random

# Monkey patch arrow's terminology
arrow.locales.EnglishLocale.timeframes["now"] = "now"

# Boot the app
app = Flask(__name__)
app.config.from_pyfile("settings.cfg")
redis = StrictRedis(app.config["REDIS_HOST"], 
                    app.config["REDIS_PORT"], 
                    db=0, 
                    password=app.config["REDIS_PASSWORD"])

def request_wants_json():
    """ Nicked from http://flask.pocoo.org/snippets/45/ """
    best = request.accept_mimetypes \
        .best_match(["application/json", "text/html"])
    return best == "application/json" and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes["text/html"]

def parse_time(s, now=None):
    """ Get a time in the future from a little string """
    now = now if now else arrow.now(app.config["TIMEZONE"])
    matched = re.match(r"(?:(\d{1,3})h)?(?:(\d{1,3})m)?", s)
    hours, minutes = [int(x) if x else 0 for x in matched.groups()]
    future = now.replace(hours=+hours, minutes=+minutes)
    return future


def api_get(crs1, crs2, when):
    """ Get IPs and count close to a given time """
    key = "{}:{}".format(crs1, crs2)
    when = parse_time(when)
    t1 = when.replace(minutes=-30).timestamp
    t2 = when.replace(minutes=30).timestamp

    # Hit redis
    count = redis.zcount(key, t1, t2)
    ips = redis.zrangebyscore(key, t1, t2, withscores=False)
    name1 = stations[crs1]
    name2 = stations[crs2]

    # Output
    return {"start": {"crs": crs1, "name": name1},
            "end": {"crs": crs2, "name": name2},
            "count": count, "ips": ips, "when": when.humanize()}


def api_put(crs1, crs2, when, fake_ip=None):
    """ Register an IP at a given time """
    key = "{}:{}".format(crs1, crs2)
    ip = fake_ip if fake_ip else str(request.remote_addr)
    start_time = parse_time(when).timestamp

    # Kill IPs that are too old
    too_old = arrow.now(app.config["TIMEZONE"]).replace(
        hours=-app.config["MAX_AGE_HOURS"]).timestamp
    redis.zremrangebyscore("key", 0, too_old)

    # Add the new ip
    redis.zadd(key, start_time, ip)
    return "Created journey in {:}".format(key), 201

@app.route("/")
def index():
    if not redis.exists("cache:index"):
        page = render_template("index.html", stations=stations.values())
        redis.set("cache:index", page)
        return page
    else:
        return redis.get("cache:index")

@app.route("/create", methods=["POST"])
def create():
    crs1 = fuzzy_match(request.form["from"])[0]
    crs2 = fuzzy_match(request.form["to"])[0]
    when = request.form["when"]
    api_put(crs1, crs2, when, fake_ip="micky mouse")
    newurl = "/{}/{}/{}".format(crs1, crs2, when)

    data = api_get(crs1, crs2, when)
    return render_template("journey.html", **data)


@app.route("/<crs1>/<crs2>", methods=["GET", "PUT"])
@app.route("/<crs1>/<crs2>/<when>", methods=["GET", "PUT"])
def api(crs1, crs2, when="now"):
    crs1 = fuzzy_match(crs1)[0]
    crs2 = fuzzy_match(crs2)[0]

    if request.method == "PUT":
        api_put(crs1, crs2, when)

    data = api_get(crs1, crs2, when)
    if request_wants_json():
        return jsonify(data)
    else:
        return render_template("journey.html", **data)

@app.route("/populate")
def populate(N = 10000):
    """ Prepopulate the database """
    keys = stations.keys()
    now = arrow.now()
    p = redis.pipeline()
    for i in range(N):
        a = "lds"
        b = random.choice(keys)
        key = "{}:{}".format(a, b)
        ip = random.randint(0, 100)
        start_time = now.replace(minutes = random.randint(0, 1000)).timestamp
        p.zadd(key, start_time, ip)
    p.execute()
    return redirect("/dbview")

@app.route("/dbview")
def dbview(N=100):
    """ View the contents of the database """
    dbsize = redis.dbsize()
    keys = stations.keys()
    data = []
    for i in range(N):
        a = "lds"
        b = random.choice(keys)
        key = "{}:{}".format(a, b)
        allips = redis.zrange(key, 0, -1, withscores=True)
        allips = [(ip, arrow.get(time).humanize()) for ip, time in allips]
        data.append((stations[a], stations[b], allips))

    return render_template("dbview.html", dbsize=dbsize, keys=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
