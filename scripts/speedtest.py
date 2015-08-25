import csv
import json

def raw_data():
    """ Pre-populates Redis with a list of stations """
    with open("raw_data/RailReferences.csv") as f:
        for row in csv.reader(f):
            crs = row[2].lower()
            fullname = row[3].replace("Rail Station", "").strip()
            yield crs, fullname



if __name__ == '__main__':
    data = [{"crs":crs, "name":name} for crs, name in raw_data()]
    data = json.dumps(data)
    with open("raw_data/stations.js", "wb") as f:
        f.write("stations = {:};".format(data))

    #with open("raw_data/test.html", "w") as f:
        #for a,b in data:
            #f.write("<a href='/view/{0}'>{1}</a><br>\n".format(a, b))
