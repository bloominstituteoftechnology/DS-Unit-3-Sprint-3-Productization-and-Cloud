from flask import Flask, render_template, request
from .aq_dashboard import show_city_pm25
from flask_sqlalchemy import SQLAlchemy
from .models import Record



def create_app():
    """Create and configure an instance of the Flask Application"""
    APP = Flask(__name__)
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB = SQLAlchemy(APP)
    DB.init_app(APP)

    @APP.route('/')
    def root():
        """List of readings from Los Angeles."""

        readings = show_city_pm25('Los Angeles', 'pm25')
        return render_template('base.html', readings = readings, message='')

    @APP.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        DB.drop_all()
        DB.create_all()

        #add new readings to the database
        readings = show_city_pm25('Los Angeles', 'pm25')
        for reading in readings:
            db_reading = Record(datetime= str(reading[0]), value=str(reading[1]))
            DB.session.add(db_reading)
        DB.session.commit()
        return 'Data refreshed!'

    return APP