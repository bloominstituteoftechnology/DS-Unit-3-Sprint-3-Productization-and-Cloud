"""
Retrieve datetime and value
"""
from .models import DB, Record
import openaq

api = openaq.OpenAQ()

def add_records_refresh():
    """
    Add records to db and their values
    """
    try:
        status, body = api.measurements(city='Los Angeles', parameter='pm25',
                                        value_from=10)
        results = body['results']
        for result in results:
            db_record = Record(datetime=result['date']['utc'],
                               value=result['value'])
            DB.session.add(db_record)

    except Exception as e:
        print('Error processing {}: {}'.format(e))
        raise e
    else:
        DB.session.commit()