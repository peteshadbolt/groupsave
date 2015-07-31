import tempfile
from flask import session
import groupsavr
import unittest
import os

class APITestCase(unittest.TestCase):
    def setUp(self):
        #db_fd = tempfile.mkstemp()
        #self.db_fd, groupsavr.app.config['DATABASE'] = db_fd
        groupsavr.app.config['TESTING'] = True
        self.client = groupsavr.app.test_client()
        self.app = groupsavr.app
        #groupsavr.init_db()

    def tearDown(self):
        #os.close(self.db_fd)
        #os.unlink(groupsavr.app.config['DATABASE'])
        pass

    def test_database_setup(self):
        #con = groupsavr.connect_db()
        #cur = con.execute('PRAGMA table_info(entries);')
        #rows = cur.fetchall()
        #print rows
        #self.assertEquals(len(rows), 3)
        pass

if __name__ == '__main__':
    import nose
    nose.main()

