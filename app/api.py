import arrow
import re
from flask_restful import reqparse, abort, Api, Resource
from flask import request, make_response, jsonify
from app import app, redis, fullnames

def parse_time(s, now=None):
    """ Get a time in the future from a little string """
    now = now if now else arrow.now(app.config["TIMEZONE"])
    matched = re.match(r"(?:(\d{1,3})h)?(?:(\d{1,3})m)?", s)
    hours, minutes = [int(x) if x else 0 for x in matched.groups()]
    future = now.replace(hours=+hours, minutes=+minutes)
    return future


class JourneyItem(Resource):

    """ A journey from A to B """

    def get(self, crs1, crs2, when):
        """ Get IPs and count close to a given time """
        key = "{}:{}".format(crs1, crs2)
        when = parse_time(when)
        t1 = when.replace(minutes=-30).timestamp
        t2 = when.replace(minutes=30).timestamp

        # Hit redis
        count = redis.zcount(key, t1, t2)
        ips = redis.zrangebyscore(key, t1, t2, withscores=True)
        name1 = fullnames[crs1]
        name2 = fullnames[crs2]

        # Output
        return {"start": {"crs": crs1, "name": name1},
                "end": {"crs": crs2, "name": name2},
                "count": len(ips), "ips": ips, "when": when.humanize()}

    def put(self, crs1, crs2, when):
        """ Register an IP at a given time """
        key = "{}:{}".format(crs1, crs2)
        ip = str(request.remote_addr)
        start_time = parse_time(when).timestamp

        # Kill IPs that are too old
        too_old = arrow.now(app.config["TIMEZONE"]).replace(
            hours=-app.config["MAX_AGE_HOURS"]).timestamp
        redis.zremrangebyscore("key", 0, too_old)

        # Add the new ip
        redis.zadd(key, start_time, ip)
        return "Created journey in {:}".format(key), 201


# Setup API resource routing
api = Api(app)
api.add_resource(JourneyItem, '/api/<crs1>/<crs2>/<when>')
