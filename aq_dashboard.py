"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask

APP = Flask(__name__)

@APP.route('/')
def root():
    """Base view."""
    return 'TODO - part 2 and beyond!'
def root():
    utc_datetime =  [('2019-03-08T00:00:00.000Z', '2019-03-07T23:00:00.000Z')]
    value = [(8.13, 8.13)]
    results = zip(utc_datetime, value).str()

from flask_sqlalchemy import SQLAlchemy

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

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
