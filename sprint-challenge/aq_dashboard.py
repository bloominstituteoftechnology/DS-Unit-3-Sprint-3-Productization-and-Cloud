"""OpenAQ Air Quality Dashboard with Flask"""
from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
api = openaq.OpenAQ()

FLASK_ENV='development'
status, resp = api.measurements(city='Los Angeles', parameter='pm25')

def get_results():

	utcs = []
	for utc in range(0, len(resp['results'])):
		u = resp['results'][utc]['date']['utc']
		utcs.append(u)

	values = []
	for value in range(0, len(resp['results'])):
		v = resp['results'][value]['value']
		values.append(v)

	result = zip(utcs, values)

	return list(result)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

class Record(DB.Model):
	id = DB.Column(DB.Integer, primary_key=True)
	datetime = DB.Column(DB.String(25))
	value = DB.Column(DB.Float, nullable=False)
	def __repr(self):
		tup = (self.datetime, self.value)
		return '<Record {}>'.format(tup)

@APP.route('/')
def root():
	"""Base view."""
	lofp = str(get_results())
	return lofp

def get_data():
	dts = [Record(datetime=x[0]) for x in get_results()]
	vals = [Record(datetime=x[1]) for x in get_results()]
	DB.session.add(dts)
	DB.session.add(vals)


@APP.route('/refresh')
def refresh():
	"""Pull fresh data from Open AQ and replace existing data."""
	DB.drop_all()
	DB.create_all()
	get_data()
	DB.session.commit()
	return 'Data refreshed!'

	
	