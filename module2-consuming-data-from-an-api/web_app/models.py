

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

migrate = Migrate()


class Book(db.Model):
    __table_name__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    author_id = db.Column(db.String(128))


class User(db.Model):
    __table_name__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    
