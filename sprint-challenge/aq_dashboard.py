"""Main application and routing logic for Sprint Challenge OpenAQ."""
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests
import openaq
import pandas
from decouple import config
from .airdata import *

api = openaq.OpenAQ() 

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
DB = SQLAlchemy(APP)


@APP.route('/')
def root():
    def db_load_city():
        df_la = api.measurements(city='Los Angeles', parameter='pm25', df=True)
        load_la(df_la)
        return render_template('base.html', title='Cities Loaded')


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    for index, row in df_la.iterrows():
        measures = Record(datetime=row['date.utc'], value=row['value'])
        DB.session.add(measures)
    DB.session.commit()
    return 'Data refreshed!'