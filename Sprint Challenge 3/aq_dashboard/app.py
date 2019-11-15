"""
Build my app factory and do routes and configuration
"""

from decouple import config
from flask import Flask, render_template, request
from .models import DB, Record
from .openaq_record import add_records_refresh
from dotenv import load_dotenv
load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        records = Record.query.all()

        return render_template('base.html', title='Home', records=records)

    @app.route('/refresh', methods=['POST'])
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        records = Record.query.all()
        DB.drop_all()
        DB.create_all()
        add_records_refresh()
        message = "Records succesfully refreshed!"
        return render_template('base.html', title='Refresh', records=records,
                               message=message)

    return app