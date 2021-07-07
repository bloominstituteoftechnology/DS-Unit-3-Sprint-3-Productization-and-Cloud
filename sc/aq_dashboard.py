"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'{self.id}, {self.datetime}, {self.value}'

def get_data(city='Los Angeles', parameter='pm25'): # Added default arguments for debugging
    api = openaq.OpenAQ()
    status, body = api.measurements(city=city, parameter=parameter)
    # getting datetime values as strings
    utc = [ str(sub['date']['utc']) for sub in body['results'] ]
    # getting aq values as floats
    vals = [ float(sub['value']) for sub in body['results'] ]
    time_vals = list(zip(utc, vals))
    return time_vals

def add_to_DB(time_vals):
    for item in time_vals:
        db_object = Record(datetime=item[0], value=item[1])
        # print(item[0], item[1]) # manual debugging to ensure proper objects populating!
        DB.session.add(db_object)
        DB.session.commit()
    return db_object

@APP.route('/')
def root():
    """Base view."""
    DB.create_all()
    return render_template(
        'base.html',
        title='Home',
        display_data=f'Potentially risky: {Record.query.filter(Record.value>=10).all()}')

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    DB.session.add(add_to_DB(get_data()))
    DB.session.commit()
    return 'Data refreshed!'