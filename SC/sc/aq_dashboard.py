'''
    Import and set up the API object in your aq_dashboard.py file
    Retrieve the data from the API when the main route is called
    Create a list of (utc_datetime, value) tuples, e.g. the first two tuples for the data returned above would be: [('2019-03-08T00:00:00.000Z', 8.13), ('2019-03-07T23:00:00.000Z', 8.13)]
    Return this list in the main route, so loading the web application prints the raw list of tuples of datetimes and values
'''
import openaq
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


''' #!$#!$#!$#!$#!@$#@!$#@!

GETS, REQUESTS, ETC.

$#!$#!$#!$#!'''


def rtrn_val_utcdt(r) -> str:
    values = [x['value'] for x in r['results']]
    udt = [x['date']['utc'] for x in r['results']]

    return str(list(zip(values, udt)))


def part2() -> str:
    api = openaq.OpenAQ()

    status, resp = api.measurements(city='Los Angeles', parameter='pm25')

    return rtrn_val_utcdt(resp)


def part2_stretch(lati: float, lngi: float, radi: float) -> str:
    api = openaq.OpenAQ()

    status, resp = api.measurements(coordinates=(
        lati, lngi), radius=radi, date_from='2015-12-20', date_to='2015-12-29')

    return rtrn_val_utcdt(resp)


''' %$@%$@%$@#%$@#%$@%42

THE APP

%$@%$@%$@%$@%$@'''

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'TODO - write a nice representation of Records'


@app.route('/')
def root():
    s0 = "\n--- PART2 BASELINE --- \n\n" + part2() + '\n\n'
    la, lo, ra = (30, 40, 3)
    #s1 = f"\n--- PART2 STRETCH with args coordinates: ({la}, {lo}), radius: {ra} --- \n\n" + part2_stretch(la, lo, ra)
    return s0  # + s1


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    DB.session.commit()
    return 'Data refreshed!'
