#!/usr/bin/python
import requests
import random

if __name__ == '__main__':
    for i in range(100):
        root = "http://127.0.0.1:5000/api/"
        requests.put(root+"lds/bri/{}m".format(i)).content
