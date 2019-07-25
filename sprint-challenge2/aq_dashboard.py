"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col
import openaq

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)


# def results():
# 	utcs = [body['results'][n]['date']['utc'] for n in range(len(body['results']))]
# 	values = [body['results'][n]['value'] for n in range(len(body['results']))]
# 	tuples = list(zip(utcs, values))

# 	return tuples

@APP.route('/')
def root():
    """Base view."""
    class ItemTable(Table):
    	datetime = Col('datetime')
    	value = Col('value')
    	location = Col('location')
    items = Record.query.filter(Record.value >= 10).all()
    table = ItemTable(items)
    return table.__html__()



class Record(DB.Model):
	id = DB.Column(DB.Integer, primary_key=True)
	datetime = DB.Column(DB.String(25))
	value = DB.Column(DB.Float, nullable=False)
	location = DB.Column(DB.String(100))

	def __repr__(self):
		form = 'Date: {} --- Value: {} --- Location: {}'
		return form.format(self.datetime, self.value, self.location)

@APP.route('/refresh')
def refresh():
	""" Pull fresh data from Open AQ and replace existing data."""
	DB.drop_all()
	DB.create_all()
	api = openaq.OpenAQ()
	status, body = api.measurements(city='Los Angeles', parameter='pm25')

	ids = [i for i in range(len(body['results']))]
	dates = utcs = [body['results'][n]['date']['utc'] for n in range(len(body['results']))]
	values = [body['results'][n]['value'] for n in range(len(body['results']))]
	locations = [body['results'][n]['location'] for n in range(len(body['results']))]

	for i, d, v, l in zip(ids, dates, values, locations):
		record = Record(id=i, datetime=d, value=v, location=l)
		DB.session.add(record)
		DB.session.commit()
	return 'Data refreshed!'

