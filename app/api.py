from flask_restful import reqparse, abort, Api, Resource
from flask import request
from app import app
from app import db
from app.matrix import redis
import random

class StationItem(Resource):
    """ A single station """
    def get(self, station_id):
        sid = station_id.lower()
        fullname = redis.get(sid)
        return info

class JourneyItem(Resource):
    """ A journey from A to B """
    def get(self, a, b):
        key = "{:}/{:}".format(a.lower(), b.lower())
        members = redis.scard(key)
        return "{:} -> {:}: {:}".format(a, b, members)

    def put(self, a, b):
        key = "{:}/{:}".format(a.lower(), b.lower())
        #user = str(request.remote_addr)
        user = str(random.randint(0, 1e2))
        print "SADD {:} {:}".format(key, user)
        count = redis.sadd(key, user)
        return "Added {:} to {:}".format(user, key), 201

# Setup API resource routing 
api = Api(app)
api.add_resource(StationItem, '/api/<station_id>')
api.add_resource(JourneyItem, '/api/<a>/<b>')
