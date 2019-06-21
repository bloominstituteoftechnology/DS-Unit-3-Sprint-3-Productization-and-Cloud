"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

api = openaq.OpenAQ()

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Record {}, \n Datetime:{}, \n Value:{}> \n\n'.format(self.id,
            self.datetime, self.value)


def stuff():
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    list_of_stuff = []
    for _ in range(len(body['results'])):
        utc_datetime = body['results'][_]['date']['utc']
        value = body['results'][_]['value']
        list_of_stuff.append((utc_datetime, value))
    return list_of_stuff

def add_stuff():
    list_of_stuff = stuff()
    for _ in range(len(list_of_stuff)):
        record = Record(id = _,
                        datetime = list_of_stuff[_][0],
                        value = list_of_stuff[_][1])
        DB.session.add(record)


@APP.route('/')
def root():
    """Base view."""
    records = Record.query.filter(Record.value >= 10).all()
    return render_template('base.html', title = 'Home', records = records)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    add_stuff()
    DB.session.commit()
    return 'Data refreshed!'
