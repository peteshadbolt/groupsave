#!/usr/bin/python
from app import app
from app import api
from app.matrix import redis
import unittest
import json
import flask
import time, arrow
from app.keydefs import *

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        redis.flushdb()

    def test_list_stations(self):
        """ See that we get the expected data when listing stations """
        base = {"REMOTE_ADDR": "peepee"}
        response = self.app.get('/api/lds/shf/now', environ_base=base)
        data = json.loads(response.data)
        assert data["start"]["crs"] == "lds"
        assert data["end"]["crs"] == "shf"
        assert data["start"]["name"] == "Leeds"
        assert data["end"]["name"] == "Sheffield"
        assert data["when"] == u"just now"

    def test_put_stations(self):
        """ See that we can put stations into the DB """
        for i in range(1000):
            base = {"REMOTE_ADDR": "user{}".format(i)}
            self.app.put("/api/lds/shf/{}m".format(i), environ_base=base)

        t = time.clock()
        for i in range(100):
            data = json.loads(self.app.get("/api/lds/shf/now", environ_base=base).data)
        print "{} milliseconds per request".format(1000*(time.clock() -t)/100.)

        print data["count"]
        assert data["count"] == 1000

if __name__ == '__main__':
    import nose
    nose.main()
