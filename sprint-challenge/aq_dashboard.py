"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
from openaq import OpenAQ
import pandas as pd
from pandas.io.json import json_normalize
from flask_sqlalchemy import SQLAlchemy
from decouple import config
APP = Flask(__name__)


def create_app():
    return APP
    
def setup():
    api = OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    df = json_normalize(body['results'])
    tuples = [(x[0],x[1]) for x in df[['date.utc', 'value']].values]
    return tuples

@APP.route('/')
def root():
    """Base view."""
    s = ""
    for row in DB.session.query(Record).filter(Record.value >= 10):
        s += str(row) + " , "
    return s

@APP.route('/ladata')
def get_data():
    q = DB.session.query(Record).filter(Record.value >= 10)
    return render_template('base.html', ladata = q, title="Mark Oliver" )    
    



# APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f"Time {self.datetime} ---  Value {self.value}"


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    for o in setup():
        dgo = Record(datetime=o[0], value=o[1])
        DB.session.add(dgo)
    DB.session.commit()
    return 'Data refreshed!'    

