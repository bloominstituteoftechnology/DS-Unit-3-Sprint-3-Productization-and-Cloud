from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class Table(DB.Model):
    """Table thing"""
    pass

class Table(DB.Model):
    pass

#DB.create_all()