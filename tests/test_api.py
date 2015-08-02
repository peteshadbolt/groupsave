from groupsavr import *
import unittest
import json

class APITestCase(unittest.TestCase):
    def setUp(self):
         self.app = app.test_client()

    def tearDown(self):
        pass

    def test_list_stations(self):
        response = self.app.get('/stations')
        print response.data
        response = self.app.get('/stations/leeds')
        print response.data

if __name__ == '__main__':
    import nose
    nose.main()

