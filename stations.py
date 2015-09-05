import json
from collections import OrderedDict
import string
import re

table = string.maketrans("","")
regex = re.compile('[%s]' % re.escape(string.punctuation))

def clean(s):
    """ Clean a string """
    return regex.sub("", s.lower())

def fuzzy_match(search):
    """ Get a list of all possible codes """
    if len(search)<2: return []
    search = clean(search)
    keys = []
    if search in stations: return [search]
    for key, value in stations_clean.items():
        if search in value: keys.append(key)
    return keys

with open("data/stations.json", "rb") as f:
    print "Reading stations.json"
    d = json.load(f)
    stations = OrderedDict(d["stations"])
    stations_clean = OrderedDict(d["stations_clean"])
