"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, request
from .openaq import API, OpenAQ
from flask_sqlalchemy import SQLAlchemy

DB =SQLAlchemy()

def create_app():
    """Configure an instance of the flask application"""
    APP = Flask(__name__)
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(APP)
    #DB.drop_all()
    #DB.create_all()
    api = OpenAQ()


    @APP.route('/')
    def root():
        """Base View"""
        query_API(api=api)
        record_data = Record.query.filter(Record.value >= 10)
        return 'First 100 Tuples! :)' + str(list(record_data[:99]))
        
            


    @APP.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        DB.drop_all()
        DB.create_all()
        query_API(api=api)
        DB.session.commit()
        return 'Refreshed!'

    return APP

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '({}, {}) '.format(self.datetime, self.value)

def query_API(api):
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    for x in body['results']:
        a = tuple((x['date']['utc'], x['value']))
        b = Record(datetime=a[0], value=a[1])
        DB.session.add(b)
    DB.session.commit()

    