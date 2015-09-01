from flask import Flask
from redis import StrictRedis

app = Flask(__name__)
app.config.from_object('app.settings')

redis = StrictRedis()

#from flask.ext.sqlalchemy import SQLAlchemy
#db = SQLAlchemy(app)

from app import views, api
from fullnames import fullnames

