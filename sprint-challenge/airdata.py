"""Retrieve Tweets, embeddings, and persist in the database."""
import pandas
from decouple import config
from .aq_dashboard import DB, Record


def load_la(df_la):
    """Add or update a user *and* their Tweets, error if no/private user."""
    #DB.create_all()
    for index, row in df_la.iterrows():
        measures = Record(datetime=row['date.utc'], value=row['value'])
        DB.session.add(measures)
    DB.session.commit()