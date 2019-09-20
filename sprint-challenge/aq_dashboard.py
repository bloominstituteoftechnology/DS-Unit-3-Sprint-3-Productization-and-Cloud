"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask


APP = Flask(__name__)


@APP.route('/')
def root():
    """Base view."""
    api.measurements(city='Los Angeles', parameter='pm25')


def search():
    import openaq
    dates = utc_datetime.query.all()
    values = value.query.all()
    return render_template('base.html', title='Home', dates=dates, values=values)




from flask_sqlalchemy import SQLAlchemy

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'TODO - write a nice representation of Records'


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    DB.session.commit()
    return 'Data refreshed!'

# if __name__ == "__main__":
#     app.run(debug=True)