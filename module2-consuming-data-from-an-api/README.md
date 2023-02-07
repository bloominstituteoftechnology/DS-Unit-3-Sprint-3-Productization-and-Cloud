# Consuming Data from an API

A data-backed application is only as good as the data it has - and a great way
to get a lot of data is through an API. The idea of an API is actually very
general, but in the modern day usually refers to "asking some other service to
give you (some of) their data." A lot of apps are built this way, especially
when starting out, but there are some steps and hoops to get it working.

## Learning Objectives

- Connect to the NotTwitter API and query for tweets by various parameters
- Implement a SpaCy NLP model to create embeddings from our tweet text.

## Before Lecture

Explore the [SpaCy](https://spacy.io/usage/spacy-101). This service will let you use the [word2vect](https://en.wikipedia.org/wiki/Word2vec) to fitpredictive models such as regression to numerical data. This allows us to work with things data scientist like most - digits - opposed to unstructured words. These numbers are referred to as "embeddings" - the numbers representing the words or phrases from the vocabulary.

## Live Lecture Task

See [guided-project.md](https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud/blob/master/module2-consuming-data-from-an-api/guided-project.md)

## Assignment

See [assignment.md](https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud/blob/master/module2-consuming-data-from-an-api/assignment.md)
  

## Resources and Stretch Goals
- Add a `/user/<name>` route and template that pulls and displays user Tweets
- [Flask routing](http://flask.pocoo.org/docs/1.0/quickstart/#routing) is simple
  but powerful - take advantage of it!
- [postman](https://www.postman.com/downloads/) is an app to let you test both your
  routes and a REST API
- Make the home page a bit more useful - links to pulled users, descriptive
  text, etc.
- Make your app look nicer - the earlier mentioned [Picnic
  CSS](https://picnicss.com) is an easy way, and
  [Bootstrap](https://getbootstrap.com) is very widely used
- You may notice that pulling lots of Tweets and getting lots of embeddings
  takes a long time (and may even be rate limited) - organize your code in
  functions so these tasks can be performed "offline" (without loading the full
  Flask application)
- Try using some of the other information form the Twitter API and maybe figure out
  what information from the API might be fun to play with and store in our database.
  
  
## Twitter Developer Account
[Note about NotTwitter & NotTweepy]
