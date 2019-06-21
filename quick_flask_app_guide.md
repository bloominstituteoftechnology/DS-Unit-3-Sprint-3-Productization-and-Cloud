// make a showoff app really fast

mkdir showoff

cd showoff

pipenv --three

pipenv install flask

into vim:

from flask import flask, render_template

vim app.py
def create_app():

    @app.route("/")
    def root():
        return render_template("root.html")

    @app.route("/github")
    def github():
        return render_template("github.html")

    return app



vim __init__.py

from .app import create_app

APP = create_app()

mkdir app

mv app.py app/app.py

mv __init__.py app/__init__.py

mkdir app/templates

vim app/templates/root.html

"home page"

FLASK_APP=APP flask run



vim test.py

print("hello world")


