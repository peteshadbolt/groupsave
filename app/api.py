from flask_restful import reqparse, abort, Api, Resource
from flask import request, make_response
from app import app
from app.matrix import *
import random
import time

REQUEST_MINUTES = 5
REQUEST_LIFETIME = REQUEST_MINUTES * 60

def fullname_key(crs):
    return "fullname/{:}".format(crs)


def journey_key(crs1, crs2, minute):
    return "journey/{:}/{:}/{:}".format(crs1, crs2, minute)


def platform_key(crs, minute):
    return "platform/{:}/{:}".format(crs, minute)

class StationItem(Resource):
    """ A single station """
    def get(self, crs):
        fullname = redis.get(fullname_key(crs))

        start_time = time.time()
        minute = int(start_time // 60)
        minutes = xrange(minute - REQUEST_MINUTES, minute + REQUEST_MINUTES * 2)

        timetable = {m: redis.lrange(platform_key(crs, m), 0, -1) for m in minutes}
        timetable = {time.strftime("%A %H:%M", time.gmtime(k)): v for k, v in timetable.items() if len(v)>0}

        return {"crs": crs, "name": fullname, "timetable": timetable}

class JourneyItem(Resource):
    """ A journey from A to B """
    def get(self, crs1, crs2):
        start_time = time.time()
        minute = int(start_time // 60)
        minutes = xrange(minute - REQUEST_MINUTES, minute + REQUEST_MINUTES * 2)
        keys = [journey_key(crs1, crs2, m) for m in minutes]
        ips = redis.sunion(keys)
        count = len(ips)
        fullname1 = redis.get(fullname_key(crs1))
        fullname2 = redis.get(fullname_key(crs2))
        ips = map(int, ips)
        start = {"crs":crs1, "name":fullname1}
        end = {"crs":crs2, "name":fullname2}
        return {"start": start, "end": end, "count": count, "ips": ips}

    def put(self, crs1, crs2):
        ip = str(random.randint(0, 1e2))  #user = str(request.remote_addr)

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
api.add_resource(StationItem, '/api/<crs>')
api.add_resource(JourneyItem, '/api/<crs1>/<crs2>')

