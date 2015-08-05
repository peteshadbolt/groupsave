import requests
import time
import csv
import random

if __name__ == '__main__':
    root = "http://127.0.0.1:5000/api/"
    print requests.get(root+"yok").content
    print requests.get(root+"yok/abw").content
