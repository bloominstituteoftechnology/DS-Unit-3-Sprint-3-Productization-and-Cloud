from flask import Flask
import openaq
import json

app = Flask(__name__)

api = openaq.OpenAQ()

@app.route('/')
def index():
    status, response = api.measurements(city='Los Angeles', parameter='pm25')
    air_samples = response['results']
    dated_samples = [(sample['date']['utc'], sample['value']) for sample in air_samples]
    return str(dated_samples) 
