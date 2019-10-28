"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

DB = SQLAlchemy(APP)
API = openaq.OpenAQ()

@APP.route('/')
def root():
    """Base view."""
    return str(Record.query.all()[:5])

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    DB.session.commit()
    return 'Data refreshed!'

@APP.route('/result')
def results():
    """pull fresh data from open aq"""
    _, body = API.measurements(city="Los Angeles", parameter='pm25')
    results = []
    for result in body['results']:
        results.append((result['date']['utc'], result['value']))
    return results

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'TODO - write a nice representation of Records'
