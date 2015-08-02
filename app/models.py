from app import db

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name=None):
        self.name = name.lower().strip()

    def __repr__(self):
        return '<Station {L}>'.format(self.name)

