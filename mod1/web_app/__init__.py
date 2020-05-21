# web_app/__init__.py

from flask import Flask

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.tweet_routes import tweet_routes
from web_app.routes.twitter_routes import twitter_routes
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = "sqlite:///C:\\Users\\Mike\\LambdaSchool\\unit3\\DS-Unit-3-Sprint-3-Productization-and-Cloud\\mod1\\web_app_99.db" # using absolute filepath on Windows (recommended) h/t: https://stackoverflow.com/a/19262231/670433

SECRET_KEY = os.getenv("TWITTER_API_SECRET", default="OOPS")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(tweet_routes)
    app.register_blueprint(twitter_routes)
    return app

@app.route('/iris')
def iris():    
    from sklearn.datasets import load_iris
    from sklearn.linear_model import LogisticRegression
    X, y = load_iris(return_X_y=True)
    clf = LogisticRegression(random_state=0, solver='lbfgs',
                          multi_class='multinomial').fit(X, y)

 return str(clf.predict(X[:2, :]))

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)