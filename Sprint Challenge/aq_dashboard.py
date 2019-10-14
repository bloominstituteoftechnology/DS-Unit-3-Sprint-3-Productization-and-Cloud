"""OpenAQ Air Quality Dashboard with Flask."""
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)


APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    utc_datetime = DB.Column(DB.DateTime(timezone=True))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'< Time {self.utc_datetime} --- Value {self.value} >'


def get_measurements(city='Los Angeles', parameter='pm25'):
    api = openaq.OpenAQ()
    status, body = api.measurements(city=city, parameter=parameter)
    return [(datetime.strptime(result['date']['utc'],
                               '%Y-%m-%dT%H:%M:%S.%f%z'),
             result['value']) for result in body['results']]


@APP.route('/')
def root():
    """Base view."""
    return str(get_measurements())


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    data = get_measurements()
    for record in data:
        DB.session.add(Record(utc_datetime=record[0], value=record[1]))
    DB.session.commit()
    return 'Data refreshed!'
