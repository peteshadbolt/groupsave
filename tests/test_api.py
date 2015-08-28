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
        pass

    def test_list_stations(self):
        response = self.app.get('/api/lds/shf/now')
        data = json.loads(response.data)
        assert data["start"]["crs"] == "lds"
        assert data["end"]["crs"] == "shf"
        assert data["start"]["name"] == "Leeds"
        assert data["end"]["name"] == "Sheffield"
        assert data["when"] == "now"

if __name__ == '__main__':
    import nose
    nose.main()
