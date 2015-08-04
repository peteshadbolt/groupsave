import requests
import time

if __name__ == '__main__':
    root = "http://127.0.0.1:5000/api/"
    print requests.get(root+"yok").content
    print requests.get(root+"yok/abw").content
    print requests.put(root+"yok/abw").content
