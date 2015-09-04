#!/usr/bin/python
import requests
import random

if __name__ == '__main__':
    for i in range(10):
        root = "http://127.0.0.1:5000/api/"
        print root+"lds/shf/{}m".format(i)
        requests.put(root+"lds/shf/{}m".format(i)).content
