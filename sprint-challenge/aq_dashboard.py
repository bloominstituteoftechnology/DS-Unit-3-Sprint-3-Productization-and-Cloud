"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq
import requests

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)
API = openaq.OpenAQ()

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<datetime:{}, value:{}>'.format(self.datetime, self.value)


def get_utc_pm(city='Los Angeles', paramater='pm25'):
    status, body = API.measurements()
    values = []
    for result in body['results']:
        date_utc = result['date']['utc']
        value = result['value']
        values.append((date_utc, value))
    return values

@APP.route('/')
def root():
    answers = Record.query.filter(Record.value >= 10.0).all()
    return str(answers)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    data = get_utc_pm()
    for i in data:
        record = Record(datetime=i[0], value=i[1])
        DB.session.add(record)
    DB.session.commit()

    return 'Data refreshed!'
