from redis import StrictRedis
import csv

def populate():
    """ Pre-populates Redis with a list of stations """
    with open("raw_data/RailReferences.csv") as f:
        for row in csv.reader(f):
            key = row[2].lower()
            name = row[3].replace("Rail Station", "")
            name = name.strip()
            redis.set(key, name)

redis = StrictRedis()
if redis.dbsize()==0:
    populate()

