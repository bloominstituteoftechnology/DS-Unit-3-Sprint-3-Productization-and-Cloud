"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq

APP = Flask(__name__)
API = openaq.OpenAQ()


@APP.route('/')
def root():
    """Base view."""
    # return 'TODO - part 2 and beyond!'
    los_angeles_data = get_los_angeles_data()
    return str(los_angeles_data)

@APP.route('/main')
def get_los_angeles_data():
    """ Retrieves 100 observations of measurements of fine particulate
    matter (PM 2.5) in the Los Angeles area."""
    status, body = API.measurements(city='Los Angeles', parameter='pm25')
    dt_values_tups_list = [(dic['date']['utc'], dic['value']) for
                           dic in body['results']]

    return dt_values_tups_list
