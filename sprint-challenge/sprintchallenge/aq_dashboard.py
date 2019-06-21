"""Functions to display openaq data."""
from .openaq import OpenAQ
#!/usr/bin/env python
# -*- coding: utf-8 -*-

def show_city_pm25(city, paramater):

    api = OpenAQ()

    status, body = api.measurements(city=city, paramater=paramater)

    time_results_list = []

    for result in body['results']:

        utc = result['date']['utc']
        value = result['value']
        time_results_list.append((utc, value))

    return time_results_list
    





