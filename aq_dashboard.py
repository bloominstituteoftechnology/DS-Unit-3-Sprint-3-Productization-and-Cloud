"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from openaq_py import API, OpenAQ
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)

@APP.route('/')
def root():
    return Record.query.filter(Record.value >=10).all()


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    for i in date_val():
        db_record = Record(datetime=i[0], value=i[1])
        DB.session.add(db_record)
    DB.session.commit()
    return 'Data refreshed!'


def date_val():
    status, body = api.measurements(city='Los Angeles', parameter='pm 25')
    values = []
    for i in body['results']:
        date = i['date']['utc']
        val = i['value']
        values.append((date, val))
    return values


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< Time {} ~ Value {} >'.format(self.datetime, self.value)