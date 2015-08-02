from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
db = SQLAlchemy(app)


class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Station %r>' % (self.name)


class Thing(Resource):
    """ Shows a single thing and lets you delete a thing """
    def get(self, thing_id):
        s = Station.query.filter(Station.name == thing_id).first()
        return "Here is information about " + s.name

    def delete(self, thing_id):
        s = Station.query.filter(Station.name == thing_id).first()
        db.session.delete(s)
        db.session.commit()
        return "Deleted {:}".format(thing_id), 200

    def put(self, thing_id):
        return "put", 201


class ThingList(Resource):
    """ Shows a list of all things, and lets you POST to add new things """
    def get(self):
        """ Get a list of all stations """
        all_stations = Station.query.all()
        return [s.name for s in all_stations]

    def post(self):
        """ Add a new station """
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        args = parser.parse_args()
        s = Station(**args)
        db.session.add(s)
        db.session.commit()
        return "Added {:}".format(s.name), 201


# Setup the API resource routing here
api.add_resource(ThingList, '/things')
api.add_resource(Thing, '/things/<thing_id>')

# Go
if __name__ == '__main__':
    app.run(debug=True)
