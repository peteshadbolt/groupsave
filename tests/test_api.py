#!/usr/bin/python
from app import app
from app import api
import unittest
import json
import flask


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
        assert data["when"] == "now"

    def test_put_stations(self):
        """ See that we can put stations into the DB """
        for i in range(100):
            base = {"REMOTE_ADDR": "user{}".format(i)}
            response = self.app.put('/api/lds/shf/now', environ_base=base)


if __name__ == '__main__':
    import nose
    nose.main()
