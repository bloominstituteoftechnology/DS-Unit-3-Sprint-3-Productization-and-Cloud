"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openaq

api = openaq.OpenAQ()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)

def report_air(city='Los Angeles', parameter='pm25'):
    """get data from openaq API"""
    status, body = api.measurements(city=city, parameter=parameter)
    results = []
    for result in body['results']:
        datetime = result['date']['utc']
        value = result['value']
        results.append((datetime, value))
    return results

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<DateTime: {} | Value: {}>'.format(self.datetime, self.value) 

@app.route('/')
def root():
    """Base view."""
    records = Record.query.filter(Record.value >= 10).all()
    # Stretch Goal Part 4 using templates
    return render_template('base.html', records=records)

@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    results = report_air()
    for i in results:
        record = Record(datetime=i[0], value=i[1])
        DB.session.add(record)
    DB.session.commit()
    return 'Data refreshed!'