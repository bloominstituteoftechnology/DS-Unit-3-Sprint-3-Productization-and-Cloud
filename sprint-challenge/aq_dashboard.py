"""OpenAQ Air Quality Dashboard with Flask."""

import openaq
from flask import Flask

APP = Flask(__name__)


def query_aq():
    """Queries OpenAQ for air quality data in Los Angeles and parses tuple data via nested key extraction"""
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    results = []
    utc_list = []
    value_list = []

    x = 0
    for result in body['results']:

        results.append(body['results'][x])
        utc_list.append(results[x]['date']['utc'])
        value_list.append(results[x]['value'])
        x = x + 1
    # BULLY, lists cannot be rendered.
    return tuple(zip(utc_list, value_list))


@APP.route('/')
def root():
    """Base view. Uses utility functions to return Air Quality data and serves to Flask for web rendering"""

    return str(query_aq())

print(query_aq())