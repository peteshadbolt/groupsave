#!/usr/bin/python
from gs import app, redis
import unittest
import json
import flask
import time
import arrow


class APITestCase(unittest.TestCase):

    def setUp(self):
        """ Pre testing """
        self.app = app.test_client()

    def tearDown(self):
        """ Post testing """
        redis.flushdb()

    def test_accept_behaviour(self):
        """ See that Accept headers are obeyed """
        base = {"REMOTE_ADDR": "test"}
        headers = [("Accept", "application/json")]
        response = self.app.get(
            '/lds/shf/now', environ_base=base, headers=headers)
        assert response.data.startswith("{")
        headers = [("Accept", "text/html")]
        response = self.app.get(
            '/lds/shf/now', environ_base=base, headers=headers)
        assert response.data.startswith("<!DOCTYPE html>")

    def test_list_stations(self):
        """ See that we get the expected data when listing stations """
        base = {"REMOTE_ADDR": "test"}
        headers = [("Accept", "application/json")]
        response = self.app.get(
            '/lds/shf/now', environ_base=base, headers=headers)
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["start"]["crs"] == "lds"
        assert data["end"]["crs"] == "shf"
        assert data["start"]["name"] == "Leeds"
        assert data["end"]["name"] == "Sheffield"
        assert data["when"] == u"now"

    def test_put_stations(self, N=100):
        """ Check that we can dump a load of stations in the DB and read them out """
        # Add a load of users with fake IPs
        for i in range(N):
            base = {"REMOTE_ADDR": "user{}".format(i)}
            self.app.put("/lds/shf/{}m".format(i), environ_base=base)

        base = {"REMOTE_ADDR": "test"}
        headers = [("Accept", "application/json")]

        # Get an interval and check that we see the right number of people
        data = json.loads(
            self.app.get("/lds/shf/now", environ_base=base, headers=headers).data)
        assert data["count"] == app.config["LIFETIME_MINUTES"] + 1
        assert data["when"] == "now"
        assert data["start"] == {"crs": "lds", "name": "Leeds"}
        assert data["end"] == {"crs": "shf", "name": "Sheffield"}


if __name__ == '__main__':
    import nose
    nose.main()
