"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy
import sqlite3


def clean_data(data):
    tuple_list = []
    for piece in data:
        tuple_list.append((piece['date']['utc'], piece['value']))
    return dict(tuple_list)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)
DB.init_app(app)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<DateTime {} Value {}>.format(self.datetime, self.value)'

@app.route('/')

def root():
    #api = openaq.OpenAQ()
    #status, body = api.measurements(city='Los Angeles', parameter='pm25')
    #dirty_data = body['results']
    #data = clean_data(dirty_data)
    #return str(data)
    connection = sqlite3.connect('db.sqlite3')
    cur = connection.cursor()
    cur.execute("SELECT * FROM record WHERE value >= 10")
    rows = []
    for row in cur.fetchall():
        rows.append(row)
    return str(rows) 

@app.route('/refresh')

def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    dirty_data = body['results']
    for num in range(len(dirty_data)):
        new_data = Record(datetime= dirty_data[num]['date']['utc'], value = dirty_data[num]['value'])
        DB.session.add(new_data)
    DB.session.commit()
    return 'Data refreshed!'



if __name__ == '__main__':
    app.run(port=9000, debug= True)