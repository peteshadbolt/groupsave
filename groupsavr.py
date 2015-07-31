from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

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
    """ Shows a list of all things, and lets you POST to add new tasks """
    def get(self):
        return "get list"

    def post(self):
        return "post list", 201

# Setup the API resource routing here
api.add_resource(ThingList, '/things')
api.add_resource(Thing, '/things/<thing_id>')

if __name__ == '__main__':
    app.run(debug=True)
