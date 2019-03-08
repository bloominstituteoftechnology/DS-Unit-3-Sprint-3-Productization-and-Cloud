"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq

APP = Flask(__name__)
api = openaq.OpenAQ()


@APP.route('/')
def root():
    """Base view."""
    return 'TODO - part 2 and beyond!'

@APP.route('/main')
def get_los_angeles_data():
    """ Retrieves 100 observations of measurements of fine particulate
    matter (PM 2.5) in the Los Angeles area."""
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    dt_values_tups_list = [(dic['date'], dic['value']) for dic in body['results']]

    return str(dt_values_tups_list)
