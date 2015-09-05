"""
Builds list of stations
"""
import json
import pandas
from stations import clean

def numerate(x):
    """ Convert a dumbass string to a number """
    try:
        return int(x.replace(",", ""))
    except ValueError:
        return None

def usage_data():
    """ Get pertinent columns from usage data """
    df = pandas.read_csv("data/station_usage_2013.csv", delimiter=",")
    tlc = df["Origin TLC"].apply(str.lower)
    count = df["Entries Full"].apply(numerate)
    name = df["Station Name"]
    return zip(tlc, name, count)

if __name__ == '__main__':
    sorted_data = sorted(usage_data(), key=lambda x: x[2], reverse=True)
    data = [[crs, name] for crs, name, score in sorted_data]
    clean_data = [[crs, clean(name)] for crs, name, score in sorted_data]

    # Dump to disk
    with open("stations.json", "wb") as f:
        json.dump({"stations":data, "stations_clean":clean_data}, f)
