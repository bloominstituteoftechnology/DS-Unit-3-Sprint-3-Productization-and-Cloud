"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, request, render_template
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
api = openaq.OpenAQ()
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

@APP.route('/')
def root():
    records = Record.query.filter(Record.value>= 10).all()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    cities = []
    for location in body["results"]:
        cities.append( { str(location['date']['utc']): str(location['value']) } )

    recordlist = []
    for record in records:
        recordlist.append({record.id:record.value})

    return render_template('base.html')
    return '\n'.join(map(str, recordlist))

@APP.route('/search', methods=['POST'])
def search(country='US', city='Los Angeles', parameter='pm25'):
    country = request.values['country_name']
    city = request.values['city_name']

    status, body = api.measurements(countries=country,city=city, parameter=parameter)
    return body

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Value {}>'.format(self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()

    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    if status == 200:
        for i in range(len(body["results"])):
            record = (Record(id=i, datetime=body['results'][i]['date']['utc'], value=body['results'][i]['value']))
            DB.session.add(record)

    DB.session.commit()
    return 'Data refreshed!'