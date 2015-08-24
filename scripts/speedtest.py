import csv
import json

def raw_data():
    """ Pre-populates Redis with a list of stations """
    with open("raw_data/RailReferences.csv") as f:
        for row in csv.reader(f):
            crs = row[2].lower()
            fullname = row[3].replace("Rail Station", "").strip().lower()
            yield crs, fullname



if __name__ == '__main__':
    data = [[crs, name] for crs, name in raw_data()]
    with open("raw_data/stations.json", "wb") as f:
        json.dump(data, f)
