"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'ID {}, DateTime {}, value {}'.format(self.id, self.datetime, self.value)


@APP.route('/')
def root():
    """Base view."""
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    n = len(body['results'])
    utcv = [(body['results'][i]['date']['utc'], body['results'][i]['value']) for i in range(n)]
    return str(Record.query.filter(Record.value >= 10).all())
    #return str(utcv)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    n = len(body['results'])
    utcv = [(body['results'][i]['date']['utc'], body['results'][i]['value']) for i in range(n)]
    for i in range(n):
        dt = utcv[i][0]
        val = utcv[i][1]
        DB.session.add(Record(datetime=dt, value=val))
    DB.session.commit()
    return 'Data refreshed!'
