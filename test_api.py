import tempfile
from flask import session
import groupsavr
import unittest
import database
import os

class APITestCase(unittest.TestCase):
    def setUp(self):
        #db_fd = tempfile.mkstemp()
        #self.db_fd, groupsavr.app.config['DATABASE'] = db_fd
        app = groupsavr.get_app()
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.app = app
        database.init_db()

    def tearDown(self):
        pass

    def test_database_setup(self):
        pass

if __name__ == '__main__':
    import nose
    nose.main()

