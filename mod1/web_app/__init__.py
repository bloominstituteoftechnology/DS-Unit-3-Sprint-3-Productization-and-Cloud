# web_app/__init__.py

from flask import Flask

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.tweet_routes import tweet_routes

DATABASE_URI = "sqlite:///C:\\Users\\Mike\\LambdaSchool\\DS-Unit-3-Sprint-3-Productization-and-Cloud\\mod1\\web_app_99.db" # using absolute filepath on Windows (recommended) h/t: https://stackoverflow.com/a/19262231/670433

SECRET_KEY = "TWITTER_API_SECRET" # todo: use env var to customize

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(tweet_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)