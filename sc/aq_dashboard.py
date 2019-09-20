"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

# set up API object
api = openaq.OpenAQ()

# retrieve data from API and put into list
# return [('2019-03-08T00:00:00.000Z', 8.13), ('2019-03-07T23:00:00.000Z', 8.13)]
status, body = api.measurements(city='Los Angeles', parameter='pm25')

list = []

for result in body['results']:
    list.append((result['date']['utc'], result['value']))


# last step, query database for any Record objects
# that have a value greater or equal to 10



@APP.route('/')
def root():
    """Base view."""
    # print raw list of tuples of datetimes and values
    filtered = str(Record.query.filter(Record.value >= 10).all())
    return render_template('base.html', title='Home', filtered=filtered)


APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'< Time {self.datetime} --- Value {self.value} >'

# the list contains tuples of each record
# what we want is first store the datetime as a str
# and value as a float into the list 'records'
# append it according to the class formats
# this makes the Record object

# then add the __repr__ method
# like '<User {}'.format(self.name)
# but format < Time 2019-03-08T01:00:00.000Z --- Value 9.48 >

# finally, add the Record object to the database

records = []

for item in list:
    records.append((Record(datetime=item[0], value=item[1])))

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    # loop through records list to add each observation to the DB
    for record in records:
        DB.session.add(record)
    DB.session.commit()
    return render_template('base.html', title='DB Refresh!')
