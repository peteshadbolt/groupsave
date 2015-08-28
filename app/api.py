from flask_restful import reqparse, abort, Api, Resource
from flask import request, make_response, jsonify
from app import app
from app.matrix import *
from app.keydefs import *
import random
import arrow
import re

REQUEST_MINUTES = 5
REQUEST_LIFETIME = REQUEST_MINUTES * 60


def get_future_time(s):
    """ Get a time in the future from a little string """
    now = arrow.now("Europe/London")
    matched = re.match(r"(?:(\d\d?)h)?(?:(\d\d?)m)?", s)
    hours, minutes = [int(x) if x else 0 for x in matched.groups()]
    now = now.replace(hours=+hours, minutes=+minutes)
    return now.humanize()


class JourneyItem(Resource):

    """ A journey from A to B """

    def get(self, crs1, crs2, when):
        # start_time = time.time()
        # minute = int(start_time // 60)
        # minutes = xrange(minute - REQUEST_MINUTES, minute + REQUEST_MINUTES * 2)
        # keys = [journey_key(crs1, crs2, m) for m in minutes]
        # ips = redis.sunion(keys)
        # count = len(ips)
        # ips = map(int, ips)

        count = 0
        ips = []
        fullname1 = redis.get(fullname_key(crs1))
        fullname2 = redis.get(fullname_key(crs2))
        start = {"crs": crs1, "name": fullname1}
        end = {"crs": crs2, "name": fullname2}
        when = when
        return {"start": start, "end": end, "count": count, "ips": ips, "when": when}

    def put(self, crs1, crs2):
        ip = str(random.randint(0, 1e2))  # user = str(request.remote_addr)

        # Timing
        start_time = time.time()
        minute = int(start_time // 60)
        expires = minute * 60 + REQUEST_LIFETIME
        expires = int(expires)

        # Journey and platform keys
        jkey = journey_key(crs1, crs2, minute)
        pkey = platform_key(crs1, minute)

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
