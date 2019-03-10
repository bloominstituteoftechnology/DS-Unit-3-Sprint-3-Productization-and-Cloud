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
    return 'TODO - part 2 and beyond!'
