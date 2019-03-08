import openaq
from flask import Flask

APP = Flask(__name__)

def los_angeles_air_quality():
#Function to pull the 10 most recent air quality tests in
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
#Create empty lists
    results = []
    float_values = []
    date_and_time = []
    
#Set x to 0 so we can limit results
    x = 0

    for result in body['results']:

        results.append(body['results'][x])
        float_values.append(float(results[x]['value'])>10)
        date_and_time.append(results[x]['date']['utc'])
        #Loop through until we hit 10
        x = x + 1
        if x == 10:
            break
    return tuple(zip(date_and_time, float_values))


@APP.route('/')
def root():
    #Function to pint the results
    return str(los_angeles_air_quality())
