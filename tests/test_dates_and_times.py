#!/usr/bin/python
import api
import unittest
import arrow

class dateTimeTestCase(unittest.TestCase):
    def test_future_time(self):
        now = arrow.now("Europe/London")
        assert api.parse_time("1h40m", now) == now.replace(hours = 1, minutes = 40)
        assert api.parse_time("50m", now) == now.replace(minutes = 50)
        assert api.parse_time("10h", now) == now.replace(hours = 10)
        assert api.parse_time("100m", now) == now.replace(minutes = 100)
        assert api.parse_time("100h", now) == now.replace(hours = 100)

class windowTestCase(unittest.TestCase):
    def test_window(self):
        now = arrow.now("Europe/London")
        pass

if __name__ == '__main__':
    import nose
    nose.main()
