"""Functions to display openaq data."""
from .openaq import OpenAQ
from .models import Record, DB
#!/usr/bin/env python
# -*- coding: utf-8 -*-

def show_city_pm25(city, paramater):

    api = OpenAQ()

    status, body = api.measurements(city=city, paramater=paramater)

    time_results_list = []

    for result in body['results']:

        utc = result['date']['utc']
        value = result['value']
        time_results_list.append((utc, value)) #, city))

    return time_results_list
    

def query_aqi_level(threshold):

    #some db results
    db_resuts = Record.query.filter(Record.value >= threshold).all()

    return db_resuts