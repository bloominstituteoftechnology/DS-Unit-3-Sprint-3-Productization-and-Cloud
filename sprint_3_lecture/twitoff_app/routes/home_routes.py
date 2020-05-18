# twitoff_app/routes/home_routes.py

from flask import Blueprint

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    x = 2 + 2
    return f"Hellow World! {x}"

@home_routes.route("/about")
def about():
    return "About me"