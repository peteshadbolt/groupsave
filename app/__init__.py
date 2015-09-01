from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app.settings')

#db = SQLAlchemy(app)

from app import views, api, matrix, fullnames

