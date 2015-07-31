from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import resources
from database import db_session


def get_app():
    app = Flask(__name__)
    api = Api(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Setup the API resource routing here
    api.add_resource(resources.ThingList, '/things')
    api.add_resource(resources.Thing, '/things/<thing_id>')
    return app

if __name__ == '__main__':
    app = get_app()
    app.run(debug=True)
