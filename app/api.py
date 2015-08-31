from flask_restful import reqparse, abort, Api, Resource
from flask import request, make_response, jsonify
from app import app
from app.matrix import *
from app.keydefs import *
import random
import arrow
import re

def parse_time(s, now=None):
    """ Get a time in the future from a little string """
    if not now: now = arrow.now("Europe/London")
    matched = re.match(r"(?:(\d{1,3})h)?(?:(\d{1,3})m)?", s)
    hours, minutes = [int(x) if x else 0 for x in matched.groups()]
    future = now.replace(hours=+hours, minutes=+minutes)
    return future


class JourneyItem(Resource):

    """ A journey from A to B """

    def get(self, crs1, crs2, when):
        start_time = parse_time(when)
        fullname1 = redis.get(fullname_key(crs1))
        fullname2 = redis.get(fullname_key(crs2))
        start = {"crs": crs1, "name": fullname1}
        end = {"crs": crs2, "name": fullname2}

        p = redis.pipeline()
        p.execute()

        return {"start": start, "end": end, "count": 0, "ips": [], "when": when}

    def put(self, crs1, crs2, when):
        # User ID
        user = str(request.remote_addr)

        # Timing
        start_time = parse_time(when)
        expires = start_time.replace(minutes = app.config["LIFETIME_MINUTES"])

        # Journey and platform keys
        jkey = journey_key(crs1, crs2, start_time)
        pkey = platform_key(crs1, start_time)

        # Dump all that into redis
        p = redis.pipeline()
        p.sadd(jkey, ip)
        p.lpush(pkey, crs2)
        p.expireat(jkey, expires)
        p.expireat(pkey, expires)
        p.execute()
        return "Created journey in {:}".format(jkey), 201

# Setup API resource routing
api = Api(app)
api.add_resource(JourneyItem, '/api/<crs1>/<crs2>/<when>')
