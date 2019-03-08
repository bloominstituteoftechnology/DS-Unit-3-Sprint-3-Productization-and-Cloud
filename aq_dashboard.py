"""OpenAQ API file dashboard Flask skewl model thing for Sprint challenge"""

from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
api = openaq.OpenAQ()
DB = SQLAlchemy(APP)
status, body = api.measurements(city='Los Angeles', parameter='pm25')

@APP.route('/')
def root():
    """Base view."""
    return body['results']

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return "Successfully recorded" + '<Record {}>'.format(self.id)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    try:
        db_pull = api.latest(city='Los Angeles', parameter='pm25')
        DB.session.add(db_pull)
        for bod in body:
            db_req = Record()
            DB.session.add(db_req)
    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e
    else:
        DB.session.commit()
        return 'Data refreshed!'


