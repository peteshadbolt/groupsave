import arrow, re
from flask_restful import reqparse, abort, Api, Resource
from flask import request, make_response, jsonify
from app import app
from app.matrix import redis
from app.keydefs import *

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
        # Figure out which keys we need to check
        when = parse_time(when)
        start = when.replace(minutes=-30)
        end = when.replace(minutes = 30)
        bins = arrow.Arrow.range("minute", start, end)
        keys = [journey_key(crs1, crs2, b) for b in bins]

        # Hit redis
        p = redis.pipeline()
        name1, name2 = redis.mget(map(fullname_key, (crs1, crs2)))
        ips = list(redis.sunion(keys))
        p.execute()

        # Output
        return {"start": {"crs": crs1, "name":name1}, 
                "end": {"crs": crs2, "name":name2}, 
                "count": len(ips), "ips": ips, "when": when.humanize()}

    def put(self, crs1, crs2, when):
        # User ID
        ip = str(request.remote_addr)

        # Timing
        start_time = parse_time(when)
        expires = start_time.replace(minutes = app.config["LIFETIME_MINUTES"]).timestamp

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
