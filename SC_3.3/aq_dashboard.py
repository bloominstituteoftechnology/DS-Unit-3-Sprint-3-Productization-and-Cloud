# OpenAQ Air Quality dashboard with Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq
import requests


APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)
API = openaq.OpenAQ()


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Record {}, \n datetime:{}, \n value:{}> \n\n'.format(self.datetime, self.value)


def get_date_particulatematter(city, parameter):
    status, body = API.measurements(city='Los Angeles', parameter='pm25')
    values = []
    for result in body['results']:
        date = result['date']['utc']
        valuetime = result['value']
        values.append((date, valuetime))
    return values


@APP.route('/')
def root():
    answers = Record.query.filter(Record.value >= 10.0).all()
    return str(answers)


@APP.route('/refresh')
def refresh():
    # pull fresh data from Open AQ and replace existing data
    DB.drop_all()
    DB.create_all()
    data = get_date_particulatematter()
    for item in data:
        record = Record(datetime=item[0], value=item[1])
        DB.session.add(record)
    DB.session.commit()

    return 'Data refreshed!'