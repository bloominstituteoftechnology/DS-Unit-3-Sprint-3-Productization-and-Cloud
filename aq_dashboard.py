"""OpenAQ Air Quality Dashboard with Flask."""
from decouple import config 
from flask import Flask, Response, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import openaq
import pandas


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    api = openaq.OpenAQ()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB = SQLAlchemy(app)
    DB.init_app(app)

    @app.route('/')
    def root():
        status, body = api.measurements(city='Los Angeles', parameter='pm25')  
        value = api.measurements(value='value')
        date = api.measurements(data='date')
        return render_template('home.html', body=body, value=value, date=date)
    
        class Record(DB.Model):

            id = DB.Column(DB.Integer, primary_key=True)
            datetime = DB.Column(DB.String(25))
            value = DB.Column(DB.Float, nullable=False)

        def __repr__(self):
            return 'TODO - write a nice representation of Records'
    
    @app.route('/refresh')
    def refresh():
        DB.drop_all()
        DB.create_all()
        DB.session.commit()
        return 'Data refreshed!'

    return app