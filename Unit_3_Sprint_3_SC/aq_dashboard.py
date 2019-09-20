"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)

api = openaq.OpenAQ()
status, body = api.cities()



aq1 = api.measurements(city='Los Angeles', parameter='pm25')[1]
aq1_tup = body['results']

results = aq1.get('results')

tup_list = []

# for res in results:
#     for_list = []
#     a = res.get('date')
#     aa = a.get('utc')
#     aaa = 'Time = ' + aa
#     b = res.get('value')
#     bb = 'Value = ' + str(b)
#     for_list.append(aaa)
#     for_list.append(bb)
#     for_list_tup = tuple(for_list)
#     tup_list.append(for_list_tup)

for res in results:
    for_list = []
    a = res.get('date')
    aa = a.get('utc')
    b = res.get('value')
    for_list.append(aa)
    for_list.append(b)
    for_list_tup = tuple(for_list)
    tup_list.append(for_list_tup)


@APP.route('/')
def root():
    """Base view."""

    return str(tup_list)


APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time: {} --- Value: {}>'.format(self.datetime, self.value)

# def add_entry(entry):
#     db_item = ()
#     DB.session.add()



@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    data = tup_list
    for ab, point in data:
        record = Record(id=ab, datetime=point[0], value=point[1])
        DB.session.add(record)
    DB.session.commit()
    return 'Data refreshed!'


# DB.drop_all()
# DB.create_all()
# # TODO Get data from OpenAQ, make Record objects with it, and add to db
# data = tup_list
# for ab, point in data:
#     record = Record(id=ab, datetime=point[0], value=point[1])
#     DB.session.add(record)
# DB.session.commit()
# print(datetime)
