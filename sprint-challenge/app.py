from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import openaq
import json

app = Flask(__name__)
db = SQLAlchemy()
openaq_api = openaq.OpenAQ()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    datetime = db.Column(db.String(25))
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Record id={} datetime={} value={}>'.format(self.id, self.datetime, self.value)

db.init_app(app)
db.create_all(app=app)

def particular_matter_samples(city):
    status, response = openaq_api.measurements(city=city, parameter='pm25')
    air_samples = response['results']
    return [(sample['date']['utc'], sample['value']) for sample in air_samples]

@app.route('/')
def index():
    return str(particular_matter_samples('Los Angeles')) 

@app.route('/refresh')
def refresh():
    db.drop_all()
    db.create_all()

    samples = particular_matter_samples('Los Angeles')
    records = [Record(datetime=date, value=measurement) for date, measurement in samples]	

    db.session.add_all(records)
    db.session.commit()

    count = db.session.execute('select count(*) from record').fetchall()[0][0]

    return 'Refreshed {} samples!'.format(count)
