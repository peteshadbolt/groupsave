#!/usr/bin/python
from gs import app, redis
import unittest
import json
import flask
import time, arrow

class APITestCase(unittest.TestCase):

    def setUp(self):
        """ Pre testing """
        self.app = app.test_client()

    def tearDown(self):
        """ Post testing """
        redis.flushdb()

    def test_list_stations(self):
        """ See that we get the expected data when listing stations """
        base = {"REMOTE_ADDR": "test"}
        response = self.app.get('/api/lds/shf/now', environ_base=base)
        data = json.loads(response.data)
        assert data["start"]["crs"] == "lds"
        assert data["end"]["crs"] == "shf"
        assert data["start"]["name"] == "Leeds"
        assert data["end"]["name"] == "Sheffield"
        assert data["when"] == u"now"

    def test_put_stations(self, N=100):
        # Add a load of users with fake IPs
        for i in range(N):
            base = {"REMOTE_ADDR": "user{}".format(i)}
            self.app.put("/api/lds/shf/{}m".format(i), environ_base=base)

        # Get an interval and check that we see the right number of people
        data = json.loads(self.app.get("/api/lds/shf/now", environ_base=base).data)
        assert data["count"]==app.config["LIFETIME_MINUTES"]+1
        assert data["when"] == "now"
        assert data["start"] == {"crs":"lds", "name":"Leeds"}
        assert data["end"] == {"crs":"shf", "name":"Sheffield"}


if __name__ == '__main__':
    import nose
    nose.main()
