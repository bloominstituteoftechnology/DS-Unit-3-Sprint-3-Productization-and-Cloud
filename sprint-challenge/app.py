from flask import Flask, abort, jsonify, request
from models import DB
import pickle

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB.init_app(APP)

@APP.route('/', methods=['GET'])
def index():
    return 'Hello, world!'

if __name__ == '__main__':
    APP.run(debug=True)

