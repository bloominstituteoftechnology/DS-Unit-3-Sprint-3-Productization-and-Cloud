"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
from .models import DB
import openaq

APP = Flask(__name__)


@APP.route('/')
def root():
    """Base view."""
    return render_template('base.html', title='Home')

@APP.route('/api')
def get_api_info():
	"""
	Add or update a user and their Tweets.
	Throw an error if user doesn't exist or private.
	"""

	api = openaq.OpenAQ()

	try:
		status, body = api.measurements(city='Los Angeles', parameter='pm25')
		results = body['results'][:2]
	except Exception as e:
		print(f'Error processing {city}, {parameter}: {e}')
		raise e
	else:
		DB.session.commit()