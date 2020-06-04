from flask import Blueprint


home_routes = Blueprint("home_routes", __name__)


@home_routes.route("/")
def index():
    print("VISITING THE HOME PAGE")
    return "Twittoff !"


@home_routes.route("/about")
def about():
    print("VISITING THE ABOUT PAGE")
    return "Twittoff App!"