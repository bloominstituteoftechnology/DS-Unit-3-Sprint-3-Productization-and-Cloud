# twitoff_app/routes/stats_routes.py

from flask import Blueprint, request, jsonify, render_template

from sklearn.linear_model import LogisticRegression # for example

from twitoff_app.models import User, Tweet
from twitoff_app.services.basilica_service import connection as basilica_connection

stats_routes = Blueprint("stats_routes", __name__)

@stats_routes.route("/predict", methods=["POST"])
def predict():
    print("PREDICT ROUTE...")
    print("FORM DATA:", dict(request.form))
    #> {'screen_name_a': 'elonmusk', 'screen_name_b': 's2t2', 'tweet_text': 'Example tweet text here'}
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]

    print("-----------------")
    print("FETCHING TWEETS FROM THE DATABASE...")
    # todo: wrap in a try block in case the user's don't exist in the database
    user_a = User.query.filter_by(screen_name = screen_name_a).one()
    user_b = User.query.filter_by(screen_name = screen_name_b).one()
    user_a_tweets = user_a.tweets
    user_b_tweets = user_b.tweets
    #user_a_embeddings = [tweet.embedding for tweet in user_a_tweets]
    #user_b_embeddings = [tweet.embedding for tweet in user_b_tweets]
    print("USER A", user_a.screen_name, len(user_a.tweets))
    print("USER B", user_b.screen_name, len(user_b.tweets))

    print("-----------------")
    print("TRAINING THE MODEL...")
    embeddings = []
    labels = []
    for tweet in user_a_tweets:
        labels.append(user_a.screen_name)
        embeddings.append(tweet.embedding)

    for tweet in user_b_tweets:
        labels.append(user_b.screen_name)
        embeddings.append(tweet.embedding)

    classifier = LogisticRegression() # for example
    classifier.fit(embeddings, labels)

    # breakpoint()
    print("-----------------")
    print("MAKING A PREDICTION...")
    #result_a = classifier.predict([user_a_tweets[0].embedding])
    #result_b = classifier.predict([user_b_tweets[0].embedding])
    #results = classifier.predict([embeddings[0]])[0] > elon

    example_embedding = basilica_connection.embed_sentence(tweet_text, model="twitter")
    result = classifier.predict([example_embedding])

    predictions = []
    tweet_texts = ["Science is awesome!", "Come check out my Tesla Model S", 
                  "The world sucks", "The government is lying to us.", 
                  "Stop the quarantine.", "Wear a mask.", "SpaceX is awesome", 
                  "Space is awesome", "I love Grimes", "Come play basketball", 
                  "Sports is the shit", "Get it Lebron!", "Come check out the game"]

    

    for text in tweet_texts:
        example_embedding = basilica_connection.embed_sentence(text, model="twitter")
        result = classifier.predict([example_embedding])
        predictions.append(result)

    # breakpoint()

    #return jsonify({"message": "RESULTS", "most_likely": result[0]})
    return render_template("results.html",
        screen_name_a=screen_name_a,
        screen_name_b=screen_name_b,
        tweet_text=tweet_text,
        screen_name_most_likely= result[0]
    )