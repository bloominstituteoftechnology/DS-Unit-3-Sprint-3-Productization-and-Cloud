"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openaq


"""Create and configure an instance of the flask app"""
APP = Flask(__name__)
api = openaq.OpenAQ()
APP.config['SQLALCHEMY_DATABASE_URI'] = 'slqite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)


@APP.route('/')
def root():
    """Base view."""

    return 'TODO - part 2 and beyond!'


def la_pm(city='Los Angeles', parameter='pm25'):
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    utc_datetime_value = []
    for result in body['results']:
        date = result['date']['utc']
        value = result['value']
        utc_datetime_value.append((date, value))

    return utc_datetime_value
