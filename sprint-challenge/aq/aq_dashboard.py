
"""OpenAQ Air Quality Dashboard with Flask."""
import openaq
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config
import requests

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(APP)
api = openaq.OpenAQ()

def results(city='Los Angeles', parameter='pm25'):
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    dictionary = body['results']
    date = []
    for i in dictionary:
        for x, y in i.items():
            if x == 'date':
                date.append(y)
    utc = []
    for i in date:
        for x, y in i.items():
            if x == 'utc':
                utc.append(y)

    value = []
    for i in value:
        for x, y in i.items():
            if x == 'value':
                value.append(x)

    measured = list(zip(utc, value))

    return measured


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {} --- Value {}>'.format(self.datetime, self.value)

@APP.route('/')
def root():
    return "Homepage"

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    a = results(city='Los Angeles', parameter='pm25')
    for i in a:
        m = Record(datetime=i[0], value=i[1])
        DB.session.add(m)
    DB.session.commit()
    return 'Data refreshed!'


    return APP
