import tempfile
from flask import session
import api
import unittest
import os

class APITestCase(unittest.TestCase):

    def setUp(self):
        db_fd = tempfile.mkstemp()
        self.db_fd, api.app.config['DATABASE'] = db_fd
        api.app.config['TESTING'] = True
        self.client = api.app.test_client()
        self.app = api.app
        api.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(api.app.config['DATABASE'])

    def test_database_setup(self):
        con = api.connect_db()
        cur = con.execute('PRAGMA table_info(entries);')
        rows = cur.fetchall()
        print rows
        self.assertEquals(len(rows), 3)

    #def test_add_entries(self):
        #self.login('admin', 'secret')
        #response = self.client.post('/add', data=dict(
            #title='Hello',
            #text='This is a post'
        #), follow_redirects=True)
        #assert 'No entries here so far' not in response.data
        #assert 'Hello' in response.data
        #assert 'This is a post' in response.data

if __name__ == '__main__':
    import nose
    nose.main()

