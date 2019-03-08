"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
api = openaq.OpenAQ()
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

@APP.route('/')
def root():
    """Base view."""
    above5 = Record.query.filter(Record.value >= 5).all()
    above10 = Record.query.filter(Record.value >= 10).all()

    return render_template('home.html', 
                            above10=above10, 
                            above5=above5,
                            title='Air Quality Monitor')


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # air_stats = times_and_values()
    for x in times_and_values():
        db_record = Record(datetime=x[0], value=x[1])
        DB.session.add(db_record)
    
    DB.session.commit()
    return 'Data refreshed!'


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< Time {} --- Value {} >'.format(self.datetime, self.value)


def times_and_values(city='Los Angeles', parameter='pm25'):
    status, body = api.measurements(city=city, parameter=parameter)
    results = []
    for row in body['results']:
        date = row['date']['utc']
        value = row['value']
        results.append((date, value))
    return results