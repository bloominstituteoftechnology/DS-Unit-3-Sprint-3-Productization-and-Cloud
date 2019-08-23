"""OpenAQ Air Quality Dashboard with Flask."""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy


APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


def getdata():
    import openaq
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    list_values = [(item['date']['utc'], item['value']) for item in body['results']]
    
#     return 'TODO - part 2 and beyond!'
    return list_values

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
#         return 'TODO - write a nice representation of Records'
        return "<Time %s --- Value %s>" % (self.datetime, self.value)
    
    
@APP.route('/')
def root():
    """Base view."""
#     list_values = getdata()
#     return str(list_values)
    
    value = 10
    records = Record.query.filter(Record.value >= value).all()
    print(str(records))
    return str(records)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""    
    DB.drop_all()
    DB.create_all()
    
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    try:    
        list_values = getdata()
        for i, values in enumerate(list_values):
            record = Record(id=i, datetime=values[0],
                            value=values[1])
            DB.session.add(record)
        DB.session.commit()    
    except:
        DB.session.rollback()
        raise
    finally:
        DB.session.close()
    
    return 'Data refreshed!'