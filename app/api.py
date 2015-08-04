from flask_restful import reqparse, abort, Api, Resource
from app import app
from app import db
from models import Station

class StationItem(Resource):
    """ Shows a single station and lets you delete a station """
    def get(self, station_id):
        station_id = station_id.lower()
        s = Station.query.filter(Station.name == station_id).first()
        return "Here is information about " + s.name

    def delete(self, station_id):
        s = Station.query.filter(Station.name == station_id).first()
        db.session.delete(s)
        db.session.commit()
        return "Deleted {:}".format(station_id), 200

    def put(self, station_id):
        return "put", 201


class StationList(Resource):
    """ Shows a list of all stations, and lets you POST to add new stations """
    def get(self):
        """ Get a list of all stations """
        all_stations = Station.query.all()
        return [s.name for s in all_stations]

    def post(self):
        """ Add a new station """
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        args = parser.parse_args()
        s2 = Station.query.filter(Station.name == args.name.lower()).first()
        if s2:
            return "{:} already exists".format(args.name), 250
        else:
            s = Station(**args)
            db.session.add(s)
            db.session.commit()
            return "Added {:}".format(args.name), 201


@api.representation('application/xml')
def xml(data, code, headers):
    resp = make_response(convert_data_to_xml(data), code)
    resp.headers.extend(headers)
    return resp


# Setup API resource routing 
api = Api(app)
api.add_resource(StationList, '/stations')
api.add_resource(StationItem, '/stations/<station_id>')
