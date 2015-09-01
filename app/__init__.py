from flask import Flask
from redis import StrictRedis
from app.fullnames import fullnames

# Boot the app
app = Flask(__name__)
app.config.from_object('app.settings')

# Boot redis
redis = StrictRedis()
fullnames = fullnames

#from flask.ext.sqlalchemy import SQLAlchemy
#db = SQLAlchemy(app)
