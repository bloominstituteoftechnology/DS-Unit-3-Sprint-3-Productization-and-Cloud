"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq

APP = Flask(__name__)


def get_measurements(city='Los Angeles', parameter='pm25'):
    api = openaq.OpenAQ()
    status, body = api.measurements(city=city, parameter=parameter)
    return [(result['date']['utc'],
            result['value']) for result in body['results']]


@APP.route('/')
def root():
    """Base view."""
    return str(get_measurements())
