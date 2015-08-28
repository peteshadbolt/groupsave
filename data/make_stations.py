"""
Builds stations.js
"""
import csv
import json

#TODO: search over strings with no punctuation and deal with london properly

def usage_data():
    with open("station_usage_2013-14.csv") as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            s = row[12]
            # TODO: for crying out loud this should be a regex
            s = s.replace(",", "")
            s = s.replace("-", "")
            s = s.strip()
            count = 0 if s=="" else int(s)

            s = row[2]
            s = s.replace(",", "")
            s = s.replace("'", "")
            s = s.replace(".", "")
            s = s.replace("(", "")
            s = s.replace(")", "")
            s = s.replace("-", "")
            s = s.replace("&", "")
            name = s.strip()

            crs = row[1].lower()
            yield {"crs": crs, "name": name, "count": count}

if __name__ == '__main__':
    data = sorted(usage_data(), key=lambda x: x["count"], reverse=True)
    for i in data:
        del i["count"]

    data = [[x["crs"], x["name"]] for x in data]

    data = json.dumps(data)
    with open("stations.js", "wb") as f:
        f.write("var stations = {:};".format(data))
