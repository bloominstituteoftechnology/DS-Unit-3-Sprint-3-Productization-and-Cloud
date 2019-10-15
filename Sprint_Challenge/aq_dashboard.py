"""OpenAQ Air Quality Dashboard with Flask."""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import openaq

APP = Flask(__name__)
api = openaq.OpenAQ()

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

@APP.route('/')
def root():
    """Base view."""
    records = Record.query.filter(Record.value >= 10).all()

    return str(Record.query.all())
    #return get_tuples_list(stretch=False)

''' Part 2 '''
def get_tuples_list(city='Los Angeles', parameter='pm25', stretch=False):
    api = openaq.OpenAQ()
    status, body = api.measurements(city=city, parameter=parameter)

    tuples_list=[]
    total_obs = len(body['results'])
 
    if stretch==False:
        for obs in range(total_obs):
            tuples_list.append((
                body['results'][obs].get('date').get('utc'),
                body['results'][obs].get('value')
                ))

        return str(tuples_list)
        #return "{}".format(tuples_list)     # ALTERNATIVELY    
    else:
        #for obs in range(total_obs):
        #    tuples_list.append((
        #        body['results'][obs].get('date').get('utc'),
        #        body['results'][obs].get('value')
        #        ))
                
        return "Stretch goal"

''' Part 3 '''
class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'< Time {self.datetime} --- Value {self.value} >'

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()

    # Get tuples_list
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    tuples_list=[]
    total_obs = len(body['results'])
    for obs in range(total_obs):
        tuples_list.append((
            body['results'][obs].get('date').get('utc'),
            body['results'][obs].get('value')
            ))

    # Add to db
    total_obs = len(body['results'])
    for item in range(total_obs):
        db_record = Record(datetime=str(tuples_list[item][0]),
                           value=tuples_list[item][1])
        DB.session.add(db_record)

    DB.session.commit()
    return 'Data refreshed!'

