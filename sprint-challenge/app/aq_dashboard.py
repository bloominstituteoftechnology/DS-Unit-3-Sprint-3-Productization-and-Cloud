from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# I know it's bad to import all
from openaq_py import *

# STRETCHIEZ
# Add another interesting request to air_api w/ view to trigger and return it
# SQL does support native dateimte objects, implement that
# Simple template for those PM 2.5 values
# Forms for which city to get
# Deploy on Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(25))
    value = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'''
        Datetime: {self.datetime}
        City: {self.city}
        Country: {self.country}
        PM: {self.value}
        '''


def air_api():
    api = OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    return status, body


@app.route("/")
def root():
    """test"""
    return str(Record.query.filter(Record.value > 10).all())



@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    db.drop_all()
    db.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    _, body = air_api()
    for a in body['results']:
        list_o_items = list(a.items())
        datetimes = list(list_o_items[2][1].items())[1][1]
        readings = list_o_items[3][1]
        cities = list_o_items[0][1]
        countries = list_o_items[6][1]
        db.session.add(Record(datetime=datetimes,
                              value=readings,
                              city=cities,
                              country=countries))
    db.session.commit()
    return 'Data refreshed!'
