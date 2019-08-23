"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(app)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f"< Time {self.datetime} --- Value {self.value} >"


class CityRecord(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    city = DB.Column(DB.String(250))
    count = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return f"< City {self.city} --- Count {self.count} >"


def extract_utc_value(records):
    #print(records)
    date_value_pair = [(r['date']['utc'], r['value']) for r in records]
    
    return date_value_pair

@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    api = openaq.OpenAQ()
    
    # query LA pm25
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    if status == 200:
        pm25 = extract_utc_value(body['results'])
        for r in range(len(pm25)):
            DB.session.add(Record(id = r, datetime=pm25[r][0], value=pm25[r][1]))
    else:
        return f"ERROR: Unable to retrieve from API, status {status}"
        
    # query city name and counts
    status, body = api.cities()
    if status == 200:
        cities = body['results']
        for r in range(len(cities)):
            DB.session.add(CityRecord(id = r, city=cities[r]['city'], count=cities[r]['count']))
    else:
        return f"ERROR: Unable to retrieve from API, status {status}"
    # TODO
    DB.session.commit()
    return 'Data refreshed!'

@app.route('/refresh_cities')
def refresh_cities():
    api = openaq.OpenAQ()
    status, body = api.cities()
    if status == 200:
        return str(body['results'])
    else:
        return f"ERROR: Unable to retrieve from API, Status {status}"

@app.route('/cities')
def cities():
    out = CityRecord.query.all()
    return str(out)

@app.route('/')
def root():
    """Base view."""
    out = Record.query.filter(Record.value >= 10).all()
    
    return str(out)
    
    
if __name__ == "__main__":
    app.run(debug = True)