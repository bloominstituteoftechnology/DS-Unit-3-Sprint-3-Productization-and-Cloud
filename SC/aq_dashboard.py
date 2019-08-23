"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from datetime import datetime
import openaq
import sqlite3

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

def retrieve_data():
    api = openaq.OpenAQ()
    test = api.measurements(city='Los Angeles', parameter='pm25')
    number, dict = [i for i in test]
    results_dict = dict['results']
    date_dict = [i['date'] for i in results_dict]
    utc_list = [i['utc'] for i in date_dict]
    value_list = [i['value'] for i in results_dict]
    tuples_list = list(zip(utc_list, value_list))
    return str(tuples_list)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    the_value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'TODO - write a nice representation of Records'


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    api_data = retrieve_data()
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("CREATE TABLE Record (id varchar(3));")
    c.executemany('INSERT INTO Record (datetime,value) VALUES (?,?)', api_data)
    conn.commit()
    conn.close()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db

    DB.session.commit()
    return 'Data refreshed!'

@APP.route('/')
def root():
    """Base view."""
    data = retrieve_data()
    return data


if __name__ == '__main__':
    APP.run(port = 5000, debug=True)




# -----------------------------------------
def retrieve_data_2():
    api = openaq.OpenAQ()
    test = api.measurements(city='Los Angeles', parameter='pm25')
    number, dict = [i for i in test]
    results_dict = dict['results']
    date_dict = [i['date'] for i in results_dict]
    utc_list = [i['utc'] for i in date_dict]
    value_list = [i['value'] for i in results_dict]
    tuples_list = list(zip(utc_list, value_list))
    return str(utc_list), value_list

utc_list, value_list = retrieve_data_2()
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
# c.execute("CREATE TABLE Record4 (id varchar(3),datetime VARCHAR(50), value INT(10));")
# for i,j in zip(utc_list,value_list):
#     c.execute("INSERT INTO Record4 (datetime, value) VALUES ({}, {})".format(i,j))
# for entry in api_data:
#     c.executemany('INSERT INTO Record2 (datetime,value) VALUES ({},{})'.format(api_data[0],api_data[1]))
# conn.commit()
# conn.close()
# for i in api_data:

# print([x[0] for x in api_data])
# print(api_data)
# stuff, nones = zip(*api_data)
# print(type(api_data))
# print(utc_list)

