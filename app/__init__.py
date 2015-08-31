from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app.settings')
app.config.from_envvar('GROUPSAVER_SETTINGS')

db = SQLAlchemy(app)

from app import views, api, matrix

