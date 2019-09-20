"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask

APP = Flask(__name__)


@APP.route('/')
def root():
    """Base view."""

    return 'Here is where the magic will happen'

# if __name__ == "__main__":
#     app.run(debug=True)