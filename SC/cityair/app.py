"""Main application and routing logic for Open AQ."""
from decouple import config
from flask import Flask, render_template, request
from .models import DB, Measurement
from .aq_dashboard import load_measurement


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
      DB.drop_all()
      DB.create_all()
      status = load_measurement()
      message = ""
      m = Measurement.query.all()
      if status == 200:
        message = "Error loading City air quality"

      return render_template('base.html', title='Cities Air Quality',measurements=m, message=message)

    @app.route('/reset')
    def reset():
      DB.drop_all()
      DB.create_all()
      return render_template('base.html', title='DB Reset! ')


    return app

