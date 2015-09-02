from flask import Flask
from redis import StrictRedis
from fullnames import fullnames
#from flask.ext.sqlalchemy import SQLAlchemy
#db = SQLAlchemy(app)

# Boot the app
app = Flask(__name__)
app.config.from_object('settings')

# Boot redis
redis = StrictRedis()
fullnames = fullnames

import views, api

