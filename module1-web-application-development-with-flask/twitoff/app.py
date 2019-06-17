"""
main application and routing logic for  TwitOff
"""
from flask import Flask
from .model import DB

def create_app():
    """
    Create  and configure an instance of the Flask application 
    """
    app =Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route("/")
    def root():
        return 'Welcome to TwitOff!'
        
    return app