# Simple local flask instance

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    print("Welcome to this Home Page!")
    x = 2 + 2
    return f"Hello World! {x}"

@app.route("/about")
def about():
    print("What about?")
    return "About me"