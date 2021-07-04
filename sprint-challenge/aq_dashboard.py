"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openaq
import datetime

APP = Flask(__name__)
api = openaq.OpenAQ()
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy()
DB.init_app(APP)

@APP.route('/')
def root():
    """Base view."""
    pm25 = Record.query.filter(Record.value >= 10.0).all()
    return render_template('base.html', title='Air Quality', records=pm25)

@APP.route('/main')
def get_data():
    """ Retrieves 100 observations of measurements of fine particulate
    matter (PM 2.5) in the Los Angeles area."""
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    list_values = [(dic['date']['utc'], dic['value']) for dic in body['results']]
    return list_values

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {}, Value: {}>'.format(self.datetime, self.value) 

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    status, body = api.measurements(city='Los Angeles', parmeter=25)
    for i in body['results']:
        update = Record(datetime=str(i['date']['utc']), value=i['value'])
        DB.session.add(update)
    DB.session.commit()
    return "Data Refreshed!"

