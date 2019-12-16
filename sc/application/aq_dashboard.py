"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
from .openaq import API
import openaq

APP = Flask(__name__)

@APP.route('/')
def root():
    """Base view."""
    return render_template('base.html', title='Home')

@APP.route('/api')
def API():
	api = openaq.OpenAQ()
	status, body = api.measurements(city='Los Angeles', parameter='pm25')
	data = body['result']
	return data