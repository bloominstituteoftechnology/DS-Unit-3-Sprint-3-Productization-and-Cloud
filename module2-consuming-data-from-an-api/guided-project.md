# Guided Project Walkthrough

We'll get set up to access the Twitter API and add the SpaCy model to our Flask
application, using environment variables (facilitated with
[python-dotenv](https://github.com/theskumar/python-dotenv)) to ensure we don't check any secrets (API keys, passwords, etc.) into git.

## What our Flask App needs to do

Yesterday we explored the basics of routing, setting up database models (schemas) and we practiced adding some basic user and tweet data to the database. Then we queried the database when a user visited a certain route and displayed the results of the database query on the page that we served up to the web browser.

Today instead of putting fake or "dummy" data into our database, we're going to get some real user and tweet data from Twitter to add to our DB. We're also going to turn the text of those tweets into a numeric representation called "word embeddings" and save the word embeddings to the database as well. In a later module we'll use these word embeddings to train a logistic regression model.

### What the user does

1) Enter two (or more) twitter usernames.
2) Select the usernames of the accounts that they would like to compare
3) Enter some text that we would like to make a prediction with. We want to predict which user is more likely to have tweeted that text.
4) Click the "Compare Users" button to generate a prediction.

### What our app does

1) Takes the provided usernames and uses them to query the Twitter API for the users' most recent tweets.
2) Save the users and tweets from the Twitter API to our database
3) Use SpaCy to turn the text of our tweets into a numeric representation called "word embeddings"
4) Pass those word embeddings into a logistic regression to predict which user is more likely to have said that tweet.
5) Return the prediction to the user and display it on the frontend.

Today we're going to knock out the steps 1, 2, and 3 of what our app does.

## Install more libraries

Before we can make requests to the Twitter API from our app we need to install a few new python packages

- `not_tweepy` - Makes it easy to query the NotTwitter API with Python. To install this package, copy the folder `not_tweepy` to the root of your local project folder. This package is a replacement for tweepy.
- `spacy` - A whole bunch of NLP tools, but the main one that we'll be using translates text into a numeric representation called "word embeddings."
- `python-dotenv` - Reads key-value pairs from a `.env` file and sets them as environment variables within our app.

From the command line working from the root of your project folder `twitoff-DS##` run the command:

`pipenv install spacy python-dotenv`

Then feel free to start up your virtual environment

`pipenv shell`

## Generate a Twitter API Key

Log in to the [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)

In the left-hand sidebar find the "Projects & Apps" section and select the "Overview" menu item.

Scroll down until you find the "Standalone Apps" section and click the "+ Create App" button at the bottom.

![Twitter Developer Portal](/images/twitter-dev-portal.png)

Give your app a name, perhaps `"twitoff-ds##"`. And then you'll be redirected to a page that has your API Key and API Key Secret.

The API Key is like a username that identifies any API calls as coming from your application. The API Key Secret is like a password and is used to prove to twitter that we have permission to query their API.

**NEVER PUSH THE API KEY or API SECRET KEY TO GITHUB!!** Always keep this information private. In the next steps we'll go over how to use environment variables and a `.env` file to store this private information in a way that will ensure that people won't be able to see these values through the web browser and that they won't get added to GitHub.

## Using a `.env` file to store private information

Before we make the mistake of accidentally pushing these credentials to GitHub, let's store them inside of a `.env` file and update our `.gitignore` file so that can't ever happen.

From the command line working from the root of your project folder `twitoff-DS##` create a new file called `.env`.

`touch .env`

Because this filename starts with a period it is a "hidden file" (at least on MacOS). This means that you may not be able to see that this file lives within the folder unless you run the command `ls -a`. the `-a` flag modifies the `ls` command to also show hidden files (any file that starts with a period ".")

In order to make sure that git doesn't push this file to GitHub we will add it to our `.gitignore` file. In this file we can indicate anything that we don't want to be pushed to our GitHub repository. Any files or folders indicated here will be "ignored" by git commands.

Simply open your `.gitignore` file and add `.env` as its own line at the top of the file and then save the file. That's all you have to do.

If you initialized your repository on GitHub with a Python `.gitignore` file, then `.env` will automatically be included in your `.gitignore`

Now that we've ensured that the contents of this file won't ever be saved to github, let's put our API Key and Secret Key in the `.env` file. This file does not hold python but will simply hold key-value pairs that will be available within our app.

We'll also add a few other variables that will be helpful for us to have access to through environment variables within our app.

```
TWITTER_API_KEY=33QT4wvediYMPKbgt1OY3Oo7d
TWITTER_API_KEY_SECRET=ZMSUwwVVf9HvnS7u1fPwNCkyvfDEHwsbD1XCLgntZdAlA
ENV=development
DATABASE_URI=sqlite:///db.sqlite3
FLASK_APP=twitoff
NOT_TWITTER_URL=https://twitoff-be.onrender.com/
```

Notice how we don't put the values inside of quotation marks to turn them into strings? It's not necessary to store these variables as strings because this isn't a `.py` file.

Saving our Flask app's name as an environment variable makes it easier to launch the Flask python REPL. We can now start that REPL by just using the command `flask shell`.

In some situations, on some systems, in order for your environment variables to take effect, you'll need to close your command line editor and reopen it. So go ahead and shut down your virtual environment, close the terminal (or git bash) and then reopen it and restart your virtual environment. This is not typically required on Linux or Mac.

## Get tweets from the NotTwitter API and add them to our database

Let's see if we can get some not_tweets by running some code in the Python REPL.

Start the REPL.

`python`

Import the function that we'll use to retrieve our environment variables from the `.env` file.

`>>> from os import getenv`

Retrieve our API Key and API Secret and save them to variables within our REPL.

`>>> key = os.getenv('TWITTER_API_KEY')`

`>>> secret = os.getenv('TWITTER_API_KEY_SECRET')`

Import not_tweepy so that we can use it to connect to the NotTwitter API.

`>>> import not_tweepy as tweepy`

Authenticate

`>>> auth = tweepy.OAuthHandler(key, secret)`

Connect to the API using our authenticated session

`>>> twitter = tweepy.API(auth)`

Declare a user that we can query the API for.

`>>> user = 'elonmusk'`

Get a bunch of info related to the 'elonmusk' account.

`>>> twitter_user = twitter.get_user(screen_name=user)`

Let's look at all the information that we can get about the `elonmusk` twitter account.

`>>> twitter_user`

Look at the `id` of the twitter user

`>>> twitter_user.id`

Get the most recent tweets pertaining to this user

`>>> tweets = twitter_user.timeline()`

Grab the most recent tweet

`>>> tweet1 = tweets[0]`

Look at the text of elon musk's most recent tweet

`>>> tweet1.full_text`

## Add code to connect NotTwitter to our app

Within the inner `twitoff` folder create a new file called `twitter.py`

```python
'''Handles connection to NotTiwtter API using NotTweepy'''

from os import getenv
import not_tweepy as tweepy
import spacy
from .models import DB, Tweet, User

# Get API Key from environment vars.
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# Connect to the Twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)

def add_or_update_user(username):
    '''Takes username and pulls user from Twitter API'''
    twitter_user = TWITTER.get_user(screen_name=username)
    # Is there a user in the database that already has this id?
    # If not, then create a User in the database with this id.
    db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, username=username)

    # add the user to the database.
    DB.session.add(db_user)

    # get the user's tweets
    tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode='extended')

    # add each tweet to the database
    for tweet in tweets:
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300])
        db_user.tweets.append(db_tweet)
        DB.session.add(db_tweet)

    # Save the changes to the DB
    DB.session.commit()
```

Before moving on, let's test the file we just made to make sure that everything's working correctly. From the main `twitoff-DS##` open up a Flask REPL.

`flask shell`

`>>> from twitoff.twitter import add_or_update_user`

`>>> from twitoff.models import User, Tweet, DB`

`>>> add_or_update_user('elonmusk')`

`>>> User.query.all()`

If you try and add the same user multiple times you'll see that errors are thrown. In fact there's lots of ways that we could break the code that's in this file

- Try and create a user with a `screen_name` that doesn't exist on twitter.
- We won't create a new user if they already exist in the DB, but our current code will try and add the same tweets to an existing user and will throw errors when trying to add the same tweets with the same ids to the existing user.

We'll need to add some fixes for these potential bugs later on.

If we ever want a fresh start with our database, remember that we can delete what's in the database by running the code that we put in our reset route.

`>>> DB.drop_all()`

`>>> DB.create_all()`

We can also query our DB directly for elon musk as a user:

`>>> elonmusk = User.query.filter(User.username=="elonmusk")`

`>>> elonmusk = elonmusk.one()`

Look at the tweets that we added to the user

`>>> elonmusk.tweets`

See how many tweets we successfully added? Why did our code not add 200 tweets?

`>>> len(elonmusk.tweets)`

Once you've added a few users, see if they show up on the home page of the app at `localhost:5000` when you run the app.

## Get SpaCy Word Embeddings

> Note: You don't need to know anything about word embeddings for this sprint. They are not a learning objective of this sprint, but are a necessarily evil when trying to make sense of this text data. We'll explore them more fully during Unit 4 Sprint 1 -when we study some popular NLP topics.

Word embeddings are a numeric representation of text. It's really important that we be able to take text (strings) and turn them into some numeric representation that our machine learning models can use to inform their predictions.

One of the biggest challenges with word embeddings is that they are a very abstract (sometimes called a "black box") representation of the text. This means that I can't point to any single number within a set of word embeddings and tell you what that number represents. Generally the word embeddings represents all of the potential contexts in which we might see a set of words used within the english language. Word embeddings can identify words that have similar meanings by comparing the contexts that those words are found in. By "context" I mean looking at the words that commonly precede or come after an inner target word.

If you're really curious, here's [a good blog post](https://jalammar.github.io/illustrated-word2vec/) that explains more about the Word2Vec model that SpaCy is using to generate the word embeddings that we'll be working with.

We're going to download a pre-trained Spacy model that generates word embeddings, and then we'll pass that model the text of our tweets to encode the tweet text into a numeric representation.

In your `twitoff-DS##` folder run the following command to download a whole bunch of Spacy tools. This will download the toolset to your computer, not specifically to your twitoff project.

`python -m spacy download en_core_web_sm`

Save a version of the toolset that we just download to a variable called `nlp` in a python REPL.

`python`

`>>> import spacy`

`>>> nlp = spacy.load('en_core_web_sm')`

Let's get the word embeddings for a string of text

`>>> nlp("random string of text").vector`

We get back a NumPy array full of numbers that represents the linguistic contexts of the words we provided in our example string. We can use numbers like this to train a machine learning model on text.

Let's take this `nlp` model that we've downloaded and save it to its own folder (directory) within our project. We'll do this by running the following command:

`>>> nlp.to_disk('my_model')`

You should now have a new folder called `my_model` inside of your `twitoff-DS##` project folder. Now we can load this pretrained word embeddings model anywhere within our app by importing space and then running `spacy.load('my_model/')`

## Moving our Word Embeddings model into our twitter.py file

We now want to use the tweets that exist on the users that we have added to the database to generate word embeddings. We also want to save those new word embeddings to the database.

Add the following code to your twitter.py file

```python
# Load our pretrained SpaCy Word Embeddings model
nlp = spacy.load('my_model/')

# Turn tweet text into word embeddings.
def vectorize_tweets(tweet_text):
    return nlp(tweet_text).vector
```

## Add error checks to `add_or_update_user()`

Remember how our app would throw an error if we tried to add a user to our database, but there was no twitter account with that screen name? Well we can wrap parts of our `add_or_update_user()` function in what's called a `try - except` statement. The code in the `try` block will run first and if an error is thrown then the `except` block is triggered. If there is no error thrown in the `try` block then the `except` section is skipped and the `else` statement is run. In this way we will only make alterations to the DB if all of the lines in the `try` block have run successfully.

```python
def add_or_update_user(username):
    """
    Gets twitter user and tweets from twitter DB
    Gets user by "username" parameter.
    """
    try:
        # gets back twitter user object
        twitter_user = TWITTER.get_user(username)
        # Either updates or adds user to our DB
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, username=username)
        DB.session.add(db_user)  # Add user if don't exist

        # Grabbing tweets from "twitter_user"
        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="extended",
            since_id=db_user.newest_tweet_id
        )

        # check to see if the newest tweet in the DB is equal to the newest tweet from the Twitter API, if they're not equal then that means that the user has posted new tweets that we should add to our DB. 
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # tweets is a list of tweet objects
        for tweet in tweets:
            # type(tweet) == object
            # Turn each tweet into a word embedding. (vectorization)
            tweet_vector = vectorize_tweet(tweet.text)
            db_tweet = Tweet(
                id=tweet.id,
                text=tweet.text,
                vect=tweet_vector
            )
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e

    else:
        DB.session.commit()
```

## Update models.py to hold our Word Embeddings

First we'll add a `vect` column to our Tweet model. The `DB.PickleType` datatype will allow us to store the entire NumPy array of Word Embeddings in that column. We'll also need to make sure that if we already have that user in the database, that we'll only be grabbing *new* tweets from the twitter API so that we don't accidentally try and add any repeated tweets. (If we try and add tweets with the same IDs then an exception will be thrown).

```python
"""SQLAlchemy User and Tweet models for out database"""
from flask_sqlalchemy import SQLAlchemy

# creates a DB Object from SQLAlchemy class
DB = SQLAlchemy()


# Making a User table using SQLAlchemy
class User(DB.Model):
    """Creates a User Table with SQlAlchemy"""
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # name column
    username = DB.Column(DB.String, nullable=False)
    # keeps track of id for the newest tweet said by user
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return "<User: {}>".format(self.username)


class Tweet(DB.Model):
    """Keeps track of Tweets for each user"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))  # allows for text and links
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)

```

## Create an update user route on our app.py

Last but not least we'll create an `/update` route on our app that will call an `update_all_user()` function whenever it is accessed. The `update_all_users()` function will go in the twitter.py file.

```python
def update_all_users():
    usernames = []
    Users = User.query.all()
    for user in Users:
        usernames.append(user.username)
    
    return usernames
```

In the `app.py` file we'll add

```python
from .twitter import update_all_users, add_or_update_user

@app.route('/update')
def update():
    '''updates all users'''
    usernames = update_all_users()
    for username in usernames:
        add_or_update_user(username)

```
