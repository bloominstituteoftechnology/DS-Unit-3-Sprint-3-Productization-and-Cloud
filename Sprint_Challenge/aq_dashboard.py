"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
import openaq
from flask_sqlalchemy import SQLAlchemy

"""Create and configure an instance of the Flask application."""
app = Flask(__name__)
DB = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB.init_app(app)



app.config['ENV'] = 'debug'

api = openaq.OpenAQ()


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'Record {}, Date:{}, Value:{}'.format(self.id, self.datetime, self.value)

def get_time():

    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    lst=[]
    for i in body['results']:
        date = i['date']['utc']
        value = i['value']

        lst.append((date, value))
    return lst #did str(lst) initially for part 2

def add_records():
    lst = get_time()

    for i in range(len(lst)):
        new_record = Record(id = i, datetime = lst[i][0], value = lst[i][1])
        DB.session.add(new_record)

@app.route('/')
def root():
    get_times()
    r = Record.query.filter(Record.value >= 10).all()
    return render_template('home.html', title='Home', records = r)


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    add_records()
    DB.session.commit()
    return 'Data refreshed!'

@app.route('/test')
def get_times():

    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    lst=[]
    for i in body['results']:
        date = i['date']['utc']
        value = i['value']

        lst.append((date, value))

        greaterthan10 = []
    for i in lst:
        if i[1] >= 10:
            greaterthan10.append(i)
    return str(greaterthan10)
