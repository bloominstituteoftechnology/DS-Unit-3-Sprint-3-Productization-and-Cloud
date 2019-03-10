"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
api = openaq.OpenAQ()
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {}, Value: {}>'.format(self.datetime, self.value)  

@APP.route('/')
def root():
    """Base view."""
    # body = api.measurements(city='Los Angelos', parmeter=25)
    # return render_template('base.html', values=body)
    root_data = api.measurements(city='Los Angeles', parameter='pm25')
    return render_template('base.html', data1=root_data)

@APP.route('/all')
def root_all():
    """Return all records"""
    all_records = Record.query.filter().all()
    return render_template('base.html', values=all_records)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    status, body = api.measurements(city='Los Angelos', parmeter=25)
    for i in body['results']:
        update = Record(datetime=str(i['date']['utc']), value=i['value'])
        DB.session.add(update)
    DB.session.commit()
    return "Data Refreshed!"
