"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
import openaq

api = openaq.OpenAQ()
status, body = api.cities()



APP = Flask(__name__)


@APP.route('/')
def root():
    """Base view."""


    return str(api.measurements(city='Los Angeles', parameter='pm25'))

@APP.route('/status')
def status():
    api = openaq.OpenAQ()
    status, body = api.cities()
    return str(status)

@APP.route('/body')
def body():
    api = openaq.OpenAQ()
    status, body = api.cities()
    return str(body)


#
#
# #     city = cities.query.all()
# #     country = countries.query.all()
# #     dates = utc_datetime.query.all()
# #     values = value.query.all()
#
#     print(status)
#     print(body)




from flask_sqlalchemy import SQLAlchemy

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)
    cities = DB.Column(DB.String(30))
    countries = DB.Column(DB.String(30))
    measurements = DB.Column(DB.String(30))

    def __repr__(self):
        return '<Record {}>'.format(self.datetime), '<Record {}>'.format(self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""

    DB.drop_all()
    DB.create_all()
    DB.session.add(id, datetime, value, measurements)
    DB.session.commit()
    return 'Data refreshed!'

if __name__ == "__main__":
    APP.run(debug=True)