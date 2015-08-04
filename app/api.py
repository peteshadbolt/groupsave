from flask_restful import reqparse, abort, Api, Resource
from flask import request
from app import app
from app import db
from matrix import redis

class StationItem(Resource):
    """ Data on a single station """
    def get(self, station_id):
        info = redis.get(station_id.lower())
        return info

class JourneyItem(Resource):
    """ How many people are making this journey? """
    def get(self, a, b):
        key = "{:}/{:}".format(a.lower(), b.lower())
        members = redis.scard(key)
        return "{:} -> {:}: {:}".format(a, b, members)

    def put(self, a, b):
        key = "{:}/{:}".format(a.lower(), b.lower())
        user = str(request.remote_addr)
        print "SADD {:} {:}".format(key, user)
        count = redis.sadd(key, user)
        return "Added {:} to {:}".format(user, key), 201

# Setup API resource routing 
api = Api(app)
api.add_resource(StationItem, '/api/<station_id>')
api.add_resource(JourneyItem, '/api/<a>/<b>')
