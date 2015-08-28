#!/usr/bin/python
from app import app
from app import api
import unittest
import json
import flask


class dateTimeTestCase(unittest.TestCase):

    def test_future_time(self):
        print api.get_future_time("1h20m")
        #print api.get_future_time("2m") == (0, 2)
        #print api.get_future_time("1h") == (1, 0)

if __name__ == '__main__':
    import nose
    nose.main()
