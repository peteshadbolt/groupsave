#!/usr/bin/python
from flask import Flask, request, jsonify, render_template, redirect
from redis import StrictRedis
from stations import stations, stations_clean, fuzzy_match
import arrow
import re
import random

arrow.locales.EnglishLocale.timeframes["now"] = "now"

# Boot the app
app = Flask(__name__)
app.config.from_pyfile("settings.cfg")
redis = StrictRedis(app.config["REDIS_HOST"], app.config["REDIS_PORT"], db=0, password=app.config["REDIS_PASSWORD"])


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
        page = render_template("index.html", stations = stations.values())
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
    print newurl
    return redirect(newurl, code=302)

@app.route("/<crs1>/<crs2>/<when>", methods = ["GET", "PUT"])
def api(crs1, crs2, when):
    crs1 = fuzzy_match(crs1)[0]
    crs2 = fuzzy_match(crs2)[0]
    if request.method=="PUT":
        print "Put not implemented"
        pass
    data = api_get(crs1, crs2, when)
    return render_template("journey.html", **data)

@app.route("/populate")
def populate():
    keys = stations.keys()
    entries = [("lds",  random.choice(keys), random.randint(0,100)) for i in range(1000)]
    for a, b, ip in entries:
        api_put(a, b, "now", fake_ip = ip)
    return render_template("populate.html", entries = entries)

if __name__=="__main__":
    app.run(host= "0.0.0.0")
