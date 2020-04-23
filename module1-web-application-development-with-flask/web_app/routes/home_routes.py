# Imports
from flask import Blueprint

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    print("YOU VISITED INDEX")
    return "Hello Tweeters!"

@home_routes.route("/tweets")
def tweets():
    print("YOU VISITED TWEETS")
    return "Tweets (TODO)"