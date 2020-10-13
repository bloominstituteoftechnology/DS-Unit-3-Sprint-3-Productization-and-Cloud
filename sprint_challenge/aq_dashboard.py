"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import openaq

app = Flask(__name__)
api = openaq.OpenAQ()

status, body = api.measurements()

tuples = []

for item in body['results']:
    tuples.append((item['date']['utc'], item['value']))


@app.route('/')
def root():
    """Base view."""
    return str(Record.query.filter(Record.value >= 10).all())

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'Date and time: {self.datetime} --- Value {self.value}'

records = []

for item in tuples:
        records.append((Record(datetime=item[0], value=item[1])))


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    for record in records:
        DB.session.add(record)
    DB.session.commit()
    return 'Data refreshed!'
