from typing import Any

import basilica
import tweepy
from decouple import config

# first read auth handler, keys/secrets are in .env file
TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
# set access token
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
# initialize tweepy object
TWITTER = tweepy.API(TWITTER_AUTH)
# start basilica connection object
BASILICA = basilica.Connection(config("BASILICA_KEY"))


def add_or_update_user(name):
    """
	:param name: Add or update a user and their Tweets.
	:return: New or updated  user.
	Throw an error if user doesn't exist or is private
	"""
    try:
        twitter_user = TWITTER.get_user(name)
        # first check for existing, if can't do, create new one
        db_user: Any = (User.query.get(twitter_user.id) or User(
            id=twitter_user.id, name=name))
        DB.session.add(db_user)
        # list of tweet objects
        tweets = twitter_user.timeline(count=200, exclude_replies=True,
                                       include_rts=False,
                                       since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            # run basilica on each tweet
            embedding = BASILICA.embed_sentence(tweet.text, model='twitter')
            # 
            db_tweet = Tweet(id=tweet.id, text=tweet.text, embedding=embedding)
            # link to user
            db_user.tweets.append(db_tweet)
            # add to db
            DB.session.add(db_tweet)
    # this is equivalent to try-catch
    except Exception as e:
        print('Encountered error while processing {name}: {e}')
        # so anyone calling this will see error
        raise e 
    # equivalent to finally, will happen anyway
    else:
        DB.session.commit()
