# web_app/routes/book_routes.py

from flask import Blueprint, jsonify, request, render_template #, flash, redirect

tweets_routes = Blueprint("tweets_routes", __name__)

@tweets_routes.route("/tweets.json")
def list_tweets():
    tweets = [
        {"id": 1, "title": "Book 1"},
        {"id": 2, "title": "Book 2"},
        {"id": 3, "title": "Book 3"},
    ]
    return jsonify(tweets)

