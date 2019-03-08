from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy
"""
api = openaq.OpenAQ()
status, body = api.measurements(city='Los Angeles', parameter='pm25')
"""

APP = Flask(__name__)

@APP.route('/')
def root():
	api = openaq.OpenAQ()
	status, body = api.measurements(city='Los Angeles', parameter='pm25')
	body_lst = body['results'][:100]
	value = [d['value'] for d in body_lst]
	value = str(value)
	return value

@APP.route('/date')
def date_display():
	api = openaq.OpenAQ()
	status, body = api.measurements(city='Los Angeles', parameter='pm25')
	body_lst = body['results'][:100]
	utc_datetime = [d['date']['utc'] for d in body_lst]
	utc_datetime = str(utc_datetime)
	return utc_datetime

# Tina I did this separately above because the root() would not return both the utc_datetime
# and value.  I don't know why.




APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    # datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Record: {}'.format(self.value)


@APP.route('/refresh')
def refresh():
	DB.drop_all()
	DB.create_all()
	# TODO Get data from OpenAQ, make Record objects with it, and add to db
	api = openaq.OpenAQ()
	status, body = api.measurements(city='Los Angeles', parameter='pm25')
	body_lst = body['results'][:100]
	values = (d['value'] for d in body_lst)
	values = float(values)
	#utc_datetimes = [d['date']['utc'] for d in body_lst]

	for value in values:
		db_value = Record(id=id, value=value)
		DB.session.add(db_value)
		DB.session.commit()
	
	return 'Data refreshed!'

# Tina when I try to create a DataBase with the /refresh I get this error:
"""
sqlalchemy.exc.InterfaceError: (sqlite3.InterfaceError) Error binding parameter 0 - probably unsupported type. [SQL: 'INSERT INTO record (id, value) VALUES (?, ?)'] [parameters: (<built-in function id>, 2.0)] (Background on this error at: http://sqlalche.me/e/rvf5)
127.0.0.1 - - [08/Mar/2019 10:43:52] "GET /refresh HTTP/1.1" 500 -
"""

