from redis import StrictRedis
import csv
from app import app
from app.keydefs import *

def populate():
    """ Pre-populates Redis with a list of stations """
    with open("raw_data/RailReferences.csv") as f:
        for row in csv.reader(f):
            crs = row[2].lower()
            key = fullname_key(crs)
            fullname = row[3].replace("Rail Station", "").strip()
            redis.set(key, fullname)

redis = StrictRedis()
if redis.dbsize() == 0:
    populate()
