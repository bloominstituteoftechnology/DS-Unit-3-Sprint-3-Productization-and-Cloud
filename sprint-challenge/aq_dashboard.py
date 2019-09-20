"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
import openaq

api = openaq.OpenAQ()
status, body = api.cities()



APP = Flask(__name__)


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


from flask_sqlalchemy import SQLAlchemy

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)
    cities = DB.Column(DB.String(30))
    countries = DB.Column(DB.String(30))
    measurements = DB.Column(DB.String(30), primary_key=True)

    def __repr__(self):
        return '<Record {}>'.format(self.measurements)


def pull_data(city='Los Angeles', parameter='pm25'):
    status, body = api.measurements(city=city, parameter=parameter)
    values = []
    for result in body['results']:
        date_utc = result['date']['utc']
        value = result['value']
        values.append((date_utc, value))
    return values

@APP.route('/')
def root():
    records = Record.query.filter(Record.value >= 10.0).all()
    return render_template('base.html', title='', records=records)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    data = pull_data()
    for r in data:
        record = Record(datetime=r[0], value=r[1])
        DB.session.add(record)
    DB.session.commit()


if __name__ == "__main__":
    APP.run(debug=True)