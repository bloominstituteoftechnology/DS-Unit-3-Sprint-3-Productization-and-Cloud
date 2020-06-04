## Jean Fraga DS8 PR.

GitHub repo for project - https://github.com/JeanFraga/DS8_twitoff_JF

- What went well (in the context of working on the assignment) today?
- What was particularly interesting or surprising about the topic(s) today?
- What was the most challenging part of the work today, and why?

Monday- Module 1.
    1. We created a demo "hello World" web app, per tradition.
    2. For ease of use I moved this demo web app into an archives folder
        for future reference.
    3. Followed along with the lecture with minimal setbacks.
    4. Added 2 sample users with 6 different tweets using sqlite3
    Learning to use Flask is super exciting, I can't wait to see how
    it ties to Django in the future.
    I did not encounter any real challenges, I did get setback because I
    saved the "__init__" in the wrong place but after getting it into
    "TWITOFF" I was able to laucnh the flask shell and use DB to make the
    database.

Tuesday- Module 2
    1. Configured our flask application to display the user.
    2. Used the API keys given by Twitter and Basillica in our code through
        a hidden file.
    3. Wrote a `base.html` with a flask template.
    4. Wrote a python file to get the users into our database with
        `from TWITOFF.twitter import *`
        `twitter_user= TWITTER.get_user('elonmusk')`
        `tweets = twitter_user.timeline(count=200, exclude_replies=True,
            include_rts=False, tweet_mode='extended')`
        `tweets[0].text` displays one of the tweets for us to see.
    5. Reset our existing database by adding `/reset` to our flask app for
        ease.
    6. Now that we had our database ready for the tweets we want to add
        we add it with `db_user=User(id=twitter_user.id, name=twitter_user.
            screen_name, newest_tweet_id=tweets[0].id)`
        ```
        for tweet in tweets:
            embedding = BASILICA.embed_sentence(tweet.full_text,
                                                model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500],
                             embedding=embedding)
            DB.session.add(db_tweet)
            db_user.tweets.append(db_tweet)

        DB.session.add(db_user)
        DB.session.commit()
        ```

Wednesday- Module3
    1. We first added a way for the client to take an input of the twitter
        user we want to evaluate through `twitter.py` by using a function
        that relates to `base.html`. The function reads the tweets and saves
        them to the database.
    2. We added a `/user/<name>` to display the tweets that the model is using
        to make the predictions.
    3. We make a `predict.py` file and import our models, BASILICA as well as
        sklearn, numpy and Pickle(for caching).
    4. In this file we continue to make the information we have available into
        the format our LogisticRegression can process by running the tweets
        into our BASILICA(Deep neural newtowrk) that turns the sentence into
        these floats that the model can compare. (What we do here is a bit
        outside of the scope of what we have learned so far, more information
        will come in Unit 4 when we cover Machine Learning)
    5. We finish by writing the html file that will present the information
        our model finds by saying who would be more likely to say something.
    6. Then we add a form that lets the client choose between the twitter users
        available in the database to compare.
    7. As a side note, `user.html` and `prediction.html` inherit elements from
        `base.html` in order to avoid redundancy and do less work overall. Also
        The forms we add are inside `base.html`.

Thursday- Module4
    1. Today we started by testing our app with gunicorn(I was able to do this
        by running gunicorn within ubuntu WSL)
    2. We then continued to log in to heroku with `heroku login`
    3. Then we create a respository in heroku with 
        `heroku git:remote -a jeanfraga-twitoff`
    4. We verify that we have the git working with `git remote --verbose`
    5. before we can add it to heroku we create a `Procfile` with 
        `web: gunicorn TWITOFF:APP -t 120` inside. (This file is finicky
        and needs to be created without any .filetype)
    6. We also need to create the keys in heroku.com through settings, this way
        we can get .env into the heroku server to log into twitter
    7. Now we can push everything to heroku by using git with
        `git push heroku master` 
    8. We also need to create our postgres link by making the key, this can be
        automated by using `heroku addons:create heroku-postgresql:hobby-dev`
        then we can check it worked by using heroku config.
    9. Just to make sure our server didn't get the old information from sqlite
        we use `jeanfraga-twitoff.herokuapp.com/reset`