"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq
import requests

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)

api = openaq.OpenAQ()

def getmeasurements(city='Los Angeles', parameter='pm25'):
    """Fetch measurements using API"""
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    utcdate_value = []
    for result in body['results']:
        utcdate = result['date']['utc']
        value = result['value']
        utcdate_value.append((utcdate, value))

    return utcdate_value

@APP.route('/')
def root():
    """Base view."""
    # utcdate_value = getmeasurements('Los Angeles', 'pm25')
    pm25_value_gt10 = Record.query.filter(Record.value >= 10.0).all()
    return str(pm25_value_gt10)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< Time {} --- Value {} >'.format(self.datetime, self.value) 


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    utcdate_value = getmeasurements('Los Angeles', 'pm25')
    for entry in utcdate_value:
        record = Record(datetime=entry[0], value=entry[1])
        DB.session.add(record)

    DB.session.commit()
    return 'Data refreshed!'
