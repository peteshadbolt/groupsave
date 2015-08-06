from redis import StrictRedis
import csv

def station_key(sid):
    return "station:{:}".format(sid)


def journey_key(sid1, sid2):
    return "journey:{:}:{:}".format(sid1, sid2)


def journeys_key(sid):
    return "journeys:{:}".format(sid1)


def populate():
    """ Pre-populates Redis with a list of stations """
    with open("raw_data/RailReferences.csv") as f:
        for row in csv.reader(f):
            key = station_key(row[2].lower())
            name = row[3].replace("Rail Station", "")
            name = name.strip()
            redis.hmset(key, station)

redis = StrictRedis()
if redis.dbsize()==0:
    populate()

