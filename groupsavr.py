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
        return "get"

    def delete(self, thing_id):
        return "delete"

    def put(self, thing_id):
        parser = reqparse.RequestParser()
        parser.add_argument('task')
        args = parser.parse_args()
        task = {'task': args['task']}
        return "put", 201


class ThingList(Resource):
    """ Shows a list of all things, and lets you POST to add new things """
    def get(self):
        all_stations = Station.query.all()
        return [s.name for s in all_stations]

    def post(self):
        return "post list", 201


# Setup the API resource routing here
api.add_resource(ThingList, '/things')
api.add_resource(Thing, '/things/<thing_id>')

# Go
if __name__ == '__main__':
    print db
    app.run(debug=True)
