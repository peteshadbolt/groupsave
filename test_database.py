import unittest
import groupsavr
import models
import database as db

class APITestCase(unittest.TestCase):
    def setUp(self):
        app = groupsavr.get_app()
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.app = app
        db.init_db()
        #db.create_all()

    def tearDown(self):
        db.session.remove()
        #db.drop_all()

    def test_list_stations(self):
        all_stations = models.Station.query.all()
        print all_stations
        return all_stations

if __name__ == '__main__':
    import nose
    nose.main()

