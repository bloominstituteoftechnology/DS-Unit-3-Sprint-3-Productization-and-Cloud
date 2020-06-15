"""OpenAQ Air Quality Dashboard with Flask."""


from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)


@APP.route('/')
def root():
    """Base view."""
    return 'TODO - part 2 and beyond!'