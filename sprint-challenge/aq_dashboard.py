"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from openaq import OpenAQ

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)
API = OpenAQ()

@APP.route('/')
def root():
    """Base view."""
    return 'TODO - part 2 and beyond!'
