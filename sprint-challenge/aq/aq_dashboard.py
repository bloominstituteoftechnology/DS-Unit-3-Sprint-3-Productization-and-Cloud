
"""OpenAQ Air Quality Dashboard with Flask."""
from openaq import OpenAQ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config

DB = SQLAlchemy()

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

def create_app():
    APP = Flask(__name__)
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(APP)

    def __repr__(self):
        return 'TODO - write a nice representation of Records'

    @APP.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        DB.drop_all()
        DB.create_all()
        # TODO Get data from OpenAQ, make Record objects with it, and add to db
        DB.session.commit()
        return 'Data refreshed!'

    @APP.route('/')
    def root():
        api = OpenAQ()
        status, body = api.measurements(city='Los Angeles', parameter='pm25')
        # Create a list of `(utc_datetime, value)` tuples
        tup = tuple([(i.get('date').get('utc'), i.get('value')) for i in body['results']])
        return tup

    return APP
