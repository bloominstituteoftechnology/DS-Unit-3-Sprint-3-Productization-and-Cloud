
"""OpenAQ Air Quality Dashboard with Flask."""
import openaq
from app import app
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from decouple import config
import requests

# app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

DB = SQLAlchemy(app)
api = openaq.OpenAQ()

def results(city='Los Angeles', parameter='pm25'):
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    dictionary = body['results']
    date = []
    for i in dictionary:
        for x, y in i.items():
            if x == 'date':
                date.append(y)
    utc = []
    for b in date:
        for c, d in b.items():
            if c == 'utc':
                utc.append(d)

    value = []
    for p in dictionary:
        for q, r in p.items():
            if q == 'value':
                value.append(r)

    measured = list(zip(utc, value))
    return measured

@app.route('/')
def root():
    risky = Record.query.filter(Record.value >= 10).all()
    return str(risky)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< Date-time: {} - PM value: {} >'.format(self.datetime, self.value)


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    a = results(city='Los Angeles', parameter='pm25')
    for i in a:
        m = Record(datetime=i[0], value=i[1])
        DB.session.add(m)

    DB.session.commit()
    return 'Data refreshed!'
