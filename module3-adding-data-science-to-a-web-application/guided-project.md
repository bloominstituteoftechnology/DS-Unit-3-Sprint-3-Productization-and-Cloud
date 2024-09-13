# Guided Project Walkthrough

In lecture we will add predictive functionality using
[sklearn.linear_model.LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html),
training on Tweet embeddings from our database for given users. We'll accept
client requests via simple forms, and return the results with a new template. We
will start by exploring the code with a REPL or notebook, and then put as much
as we can in the application.

## Add Scikit-Learn to our project

Navigate to project folder and run

`pipenv install scikit-learn`

Then start up the virtual environment

`pipenv shell`

Then, within the `twitoff` folder create a new file called `predict.py`

`touch predict.py`

## Reset our DB Users

Start up a flask shell and we're going to run some commands to make sure we've got fresh users and tweets.

`flask shell`

Get access to users in our DB.

`>>> from twitoff.models import User, DB, Tweet`

Look at the users that are already in there.

`>>> User.query.all()`

Clear out the DB to get a fresh start.

`>>> DB.drop_all()`

`>>> DB.create_all()`

Import our add_or_update_user function.

`>>> from twitoff.twitter import add_or_update_user`

Add a couple of users.

`>>> add_or_update_user('elonmusk')`

`>>> add_or_update_user('ryanallred')`

Query the Users to make sure they were added to the DB correctly.

`>>> User.query.all()`

Query for the two users individually and save them to variables `user0` and `user1`

`>>> user0 = User.query.filter(User.username=='elonmusk').one()`

`>>> user1 = User.query.filter(User.username=='ryanallred').one()`

Look at the tweets of our two users.

`>>> user0.tweets`

`>>> len(user0.tweets)`

`>>> user1.tweets`

`>>> len(user1.tweets)`

Confirm that we have the word embeddings saved to the individual tweet objects.

`>>> user0.tweets[0].vect`

`>>> user1.tweets[0].vect`

Cool! If all of the above has run successfully for you, then you should be ready to start adding Logistic Regression functionality to your App!

## Fit a Logistic Regression

Continuing in the same Flask Shell as above, let's start preparing our word embeddings for Logistic Regression and fit our first Logistic Regression model.

Look at the shape of the word embeddings on an individual tweet

`>>> user0.tweets[0].vect.shape`

Save all of the word embeddings for a user's tweets to a variable

`>>> import numpy as np`

`>>> user0_vects = np.array([tweet.vect for tweet in user0.tweets])`

`>>> user1_vects = np.array([tweet.vect for tweet in user1.tweets])`

Look at the shape of all of a user's tweet word embeddings

`>>> user0_vects.shape`

`>>> user1_vects.shape`

Combine all of the word embeddings of the two users into one big numpy array where each row holds the embeddings of an individual tweet. This will put user0's tweets at the top and user1's tweets at the bottom of the array.

`>>> vects = np.vstack([user0_vects, user1_vects])`

`>>> vects.shape`

Create a column of labels for the tweets of the two users

`>>> labels = np.concatenate([np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])`

`>>> labels.shape`

If you think about it, we now have a `y` vector and an `X` matrix. We want to predict the label (user) from the word embeddings that pertain to that user.

Let's import Logistic Regression and fit it to this data.

`>>> from sklearn.linear_model import LogisticRegression`

`>>> log_reg = LogisticRegression()`

`>>> log_reg.fit(vects, labels)`

Let's think up a hypothetical tweet that we know is more likely to be said by one user than the other.

`>>> hypo_tweet_text = 'data science is the best'`

We'll need to get the word embeddings for the hypothetical tweet text before we can generate a prediction.

`>>> from twitoff.twitter import vectorize_tweet`

`>>> hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)`

We have a problem that the vectorization of our hypothetical tweet text is not in the correct shape for us to generate a prediction with it. Right now it has the same shape as a column of data, but we want to use it as a row of data, so we'll use NumPy to "reshape" it.

`>>> hypo_tweet_vect = np.array(hypo_tweet_vect).reshape(1,-1)`

Now let's predict which user is more likely to say the tweet!

`>>> log_reg.predict(hypo_tweet_vect)`

## Put it all into `predict.py`

```python
"""Prediction of users based on tweets"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    """
    Determine and returns which user is more likely to say a given tweet
    Example run: predict_user("elonmusk", "jackblack", "Tesla cars go vroom")
    Returns a 0 (user0_name: "elonmusk") or a 1 (user1_name: "jackblack")
    """
    # Grabbing user from our DB
    # The user we want to compare has to be in our DB
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()

    # Grabbing tweet vectors from each tweet for each user
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Vertically stack tweet_vects to get one np array
    vects = np.vstack([user0_vects, user1_vects])
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    # fit the model with our x's == vects & our y's == labels
    log_reg = LogisticRegression().fit(vects, labels)

    # vectorize the hypothetical tweet to pass into .predict()
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    return log_reg.predict(hypo_tweet_vect.reshape(1, -1))

```

## Test it out in `flask shell`

`flask shell`

`>>> from twitoff.predict import predict_user`

We can only make predictions for users that are already in our database, so let's make sure we know who those users are.

`>>> from twitoff.models import User`

`>>> User.query.all()`

`>>> predict_user('elonmusk','ryanallred','Data Science is the best!')`

## Update our frontend template

You may have noticed that the frontend (HTML) of your Twitoff app doesn't look quite the same as the demo app. We're going to fix that right now by adding a couple of new html templates to our app.

First a template that we can use to display predictions

### `prediction.html`

```html
{% extends "base.html" %}

{% block content %}
  <div id="prediction">
    <p>{{ title }}</p>
    <p>{{ message }}</p>
  </div>
{% endblock %}
```

and a template specifically for displaying user information

### `user.html`

```html
{% extends "base.html" %}

{% block content %}
<div id="user-info">
  <p>{{ title }}</p>
  <p>{{ message }}</p>
</div>

<div id="user-tweets">
  {% for tweet in tweets %}
  <span class="stack">
    {{ tweet.text }}
  </span>
  {% endfor %}
</div>
{% endblock %}
```

We will also update our base.html file to include dropdowns for selecting the two users and an input box so that the user can enter their own hypothetical tweet text

### `base.html`

```html
<!DOCTYPE html>
<html>

  <head>
    <title>TwitOff - {{ title }}</title>
    <link rel="stylesheet" href="https://unpkg.com/picnic" />
  </head>

  <body>
    <nav>
      <a href="/" class="brand"><span>TwitOff!</span></a>

      <!-- responsive-->
      <input id="bmenub" type="checkbox" class="show">
      <label for="bmenub" class="burger pseudo button">Menu</label>

      <div class="menu">
        <a href="/update" class="button warning">Update Tweets</a>
        <a href="/reset" class="button error">Reset Database</a>
      </div>
    </nav>

    <article class="flex two" style="padding: 3em 1em;">
      {% block content %}
      <div>
        <h1>{{ title }}</h1>
        <form action="/compare" method="post">
          <select name="user0">
            {% for user in users %}
            <option value="{{ user.username }}">{{ user.username }}</option>
            {% endfor %}
          </select>
          <select name="user1">
            {% for user in users %}
            <option value="{{ user.username }}">{{ user.username }}</option>
            {% endfor %}
          </select>
          <input type="text" name="tweet_text" placeholder="Tweet text to predict">
          <input type="submit" value="Compare Users">
        </form>
      </div>
      <div>
        <h2>Users</h2>
        {% for user in users %}
        <a href="/user/{{ user.name }}"><span class="stack">{{ user.name }}</span></a>
        {% endfor %}
        <form action="/user" method="post">
          <input type="text" name="user_name" placeholder="User to add">
          <input type="submit" value="Add User">
        </form>
      </div>
      {% endblock %}
    </article>
    <!-- <script src="https://cdn.jsdelivr.net/npm/umbrellajs"/> -->
  </body>

</html>
```

## Clean up our Routes

```python
"""This is what brings the application together"""
from os import getenv
from flask import Flask, render_template, request
from .predict import predict_user
from .models import DB, User, Tweet
from .twitter import add_or_update_user, get_all_usernames


def create_app():
    """
    The main app function for twitoff.
    Brings everything together.
    """
    # __name__ is the name of the current path module
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title="Home", users=User.query.all())

    @app.route('/update')
    def update():
        '''update all users'''
        usernames = get_all_usernames()
        for username in usernames:
            add_or_update_user(username)
        return "All users have been updated"

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Reset Database")

    @app.route('/user', methods=["POST"])
    @app.route('/user/<name>', methods=["GET"])
    def user(name=None, message=''):

        # we either take name that was passed in or we pull it
        # from our request.values which would be accessed through the
        # user submission
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} Successfully added!".format(name)

            tweets = User.query.filter(User.username == name).one().tweets

        except Exception as e:
            message = "Error adding {}: {}".format(name, e)

            tweets = []

        return render_template("user.html", title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values["user1"]])

        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            # prediction returns a 0 or 1
            prediction = predict_user(
                user0, user1, request.values["tweet_text"])
            message = "'{}' is more likely to be said by {} than {}!".format(
                request.values["tweet_text"],
                user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template('prediction.html', title="Prediction", message=message)

    return app
```
