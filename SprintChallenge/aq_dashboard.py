"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<<= At time {}, value was: {} =>>'.format(self.datetime, self.value)

@APP.route('/')
def root():
    """Base view."""
    return str(Record.query.filter(Record.value > 5).all()[:])
    #return 'TODO - parte deux and beyond!'

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    i=0
    for row in body['results']:
        i+=1
        date = row['date']['utc']
        value = row['value']
        db_record = Record(id=i, datetime=str(date), value=value)
        DB.session.add(db_record)
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    DB.session.commit()
    return 'Data refreshed!'
'''
Original root
@APP.route('/')
def root():
    """Base view."""
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    results = []
    for row in body['results']:
        date = row['date']['utc']
        value = row['value']
        results.append((date, value))
    return str(results)
    #return 'TODO - parte deux and beyond!'
'''