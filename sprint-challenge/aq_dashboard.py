"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
api = openaq.OpenAQ()
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


@APP.route('/')
def root():
    """Base view."""
    risky_pm25 = Record.query.filter(Record.value >= 10.0).all()
    risky_pm10 = RecordPM10.query.filter(RecordPM10.value >= 10.0).all()
    return render_template('base.html', title='Home', records=risky_pm25,
                            orecords=risky_pm10)


@APP.route('/all')
def allrecords():
    """All records view."""
    allpm25 = Record.query.filter().all()
    allpm10 = Record.query.filter().all()
    return render_template('all_rec.html', title='All Records', records=allpm25)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {} --- Value {}>'.format(self.datetime, self.value)


class RecordPM10(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {} --- Value {}>'.format(self.datetime, self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    for d in body['results']:
        new_stat = Record(datetime=str(d['date']['utc']), value=d['value'])
        DB.session.add(new_stat)
    DB.session.commit()

    status, body = api.measurements(city='Los Angeles', parameter='pm10')
    for d in body['results']:
        new_stat_pm10 = RecordPM10(datetime=str(d['date']['utc']),
                                    value=d['value'])
        DB.session.add(new_stat_pm10)
    DB.session.commit()
    return 'Data refreshed!'
