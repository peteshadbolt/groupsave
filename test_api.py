import tempfile
from flask import session
import groupsavr
import unittest
import database
import os
import models

class APITestCase(unittest.TestCase):
    def setUp(self):
        app = groupsavr.get_app()
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.app = app
        database.init_db()

    def tearDown(self):
        pass

    def test_list_stations(self):
        s = models.Station('Brighton')
        groupsavr.db_session.add(s)
        groupsavr.db_session.commit()
        all_stations = models.Station.query.all()
        print all_stations
        return all_stations

if __name__ == '__main__':
    import nose
    nose.main()

