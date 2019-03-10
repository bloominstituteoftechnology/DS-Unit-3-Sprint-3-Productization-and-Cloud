"""   """
from flask import Flask
# import matplotlib.pyplot as plt
import openaq
import pandas as pd
import requests
# import seaborn as sns

APP = Flask(__name__)

@APP.route('/')
def root():
    """Base view."""
    api_data = get_api_data()
    c = str(api_data)
    return c


def get_api_data():

    """ Query OpenAQ for LA and pm=25"""
    api = openaq.OpenAQ()
    data = []
    status, resp = api.measurements(city='Los Angeles', parameter='pm25')
    api_data = [(item['date']['utc'], item['value'])
                    for item in resp['results']]

    return api_data
