from redis import StrictRedis
import csv

def populate():
    """ Pre-populates Redis with a list of stations """
    with open("raw_data/RailReferences.csv") as f:
        for row in csv.reader(f):
            redis.set(row[2].lower(), row[3])
    print "{:} keys added to the database".format(redis.dbsize())

redis = StrictRedis()
populate()

