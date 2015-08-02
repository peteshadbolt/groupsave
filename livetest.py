import requests
import time

if __name__ == '__main__':
    root = "http://127.0.0.1:5000/"
    things = root+"things"
    print requests.get(things).content
    print requests.post(things, data={"name":"Bradford"}).content
    print requests.get(things).content
    print requests.get(things+"/Bradford").content
    print requests.delete(things+"/Bradford").content
    print requests.get(things).content
