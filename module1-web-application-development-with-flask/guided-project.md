# Guided Project Walkthrough

We're going to kick off with an overview of the major parts of a web application
(front-end, back-end, database), and then develop our own prototype web
application using Flask and SQLite. A summary of the overall picture:

- Front-end: the "look-and-feel" of an application, as well as any logic that is
  executed by client-side (browser) JavaScript (which has grown surprisingly
  powerful)
- Back-end: the routing and "business logic", where responses
  (what the client sees) are built and APIs and databases are accessed
- Database: the "source of truth", where data is persisted and updated

## "Productization" of Data Science models

![CRISP-DM Visual Guide](/images/crisp-dm.png)

What is productization?

"The process of turning a prototype of a design into a version that can be more easily mass-produced"

Productization is all about publishing our data science work in a way that helps others benefit from it. This can mean:

- Creating a written report of our analysis
- Publishing a dashboard
- Putting a trained model into a software application so that people can access it.

What are some examples of "productized" data science that you have benefitted from?

## What are Web Applications and how do they work?

Data Science models are most commonly deployed to APIs so that users of web applications can make use of their predictions. That's what we'll be doing this week! Before we dive in and start making our own simple web application, let's talk about the different parts of web apps and which of them a Data Scientist or (more realistically) a Data Engineer might need to be familiar with.

Let's check out [This blog post](https://geshan.com.np/blog/2020/02/difference-between-backend-frontend/) which I think has a good diagram that will help us see how the different parts work together.

### The "Frontend" of a Web App

The "frontend" of a web app is basically the web pages that a user interacts with through their web browser. It's always created using the same three things: HTML, CSS and JavaScript.

- HTML: The skeleton or structure of the websites, also controls the inclusion of text and images on a web page.

- CSS: Applies "styles" to the HTML that control fonts, colors, font sizes, background-colors, positions of buttons, etc.

- JavaScript: JS can be used both on the frontend and "backend" of websites, but when it exists on the frontend its job is to give websites interactivity.

You can think of HTML like the bones of a skeleton, Javascript like muscles that makes the bones move and react, and CSS like the clothes worn over the top of all of it to dress things up. Working with the frontend is **NOT** your job and is **NOT** something that I want you to worry about this week. The webapp that we make this will need at least some frontend or else there won't be anything for the users to interact with, but it's more than fine if you don't fully understand how the frontend of our webapp is working this week. Creating the frontend is not the job of a Data Scientist or Data Engineer, it's the job of a web developer.

### The "Backend" of a Web App

The "Backend" of a web app is usually divided into two main parts, the web server and the database.

Whenever we visit a web page at a specific address like <https://www.google.com/> we are making a "HTTP Request" to a web server. Our web browser reaches out to google's web server for files that exist at that address, the web server responds with HTML, CSS and JS files and then the browser composes those into what you see on your computer screen. The first job of a web server is to send respond to requests for web page files. When a user accesses a specific URL it "serves" up the web page's files.

The second job of a web server is to hold an API or "Application Programming Interface" The API's job is to respond to requests that come from the browser for *data*. An API lives on the web server and stands between the browser and our database to provide a layer of security and organization to the way in which we interact with a database. Users visiting web pages don't write SQL queries to get the data that they need, they just go about their business and then the frontend sends a HTTP request to the database -through the API- for any data that needs to be displayed on the page.

The database should be very secure and should only be accessed by approved users and applications, so the API makes that every request to the database is approved.

However, API's don't have to be only about accessing the database. They're an "interface" or code that goes between two critical parts of the application. We can also use APIs to interact with machine learning models that are stored in our web server. We can make requests to these models for predictions, just like we would make a requeset for data from the database. This week we'll be working mostly with the backend of our web app and will be building a web server that can both access a database as well as a machine learning model.

The backend of a web app can be written in many different programming languages (you'll typically just pick one that you like for a project) and there are lots of libraries/tools to help make it easier to create the web server and API. These "frameworks" are specific to the language that you're using and will lay out a specific way for us to create our backend. Each framework is a little different, this week we'll be working with a Python web development framework called "Flask."

## Getting started with our Flask App

[Here's an example version of the app that we will be building together this week.](https://github.com/LambdaSchool/TwitOff)

Create a GitHub repository called `twitoff-DS##` (replace the ## with your cohort number and clone the repo to your machine. If  GitHub SSH key isn't set up yet, just create a folder on your computer. Inside of this outer folder, createa an inner folder called `twitoff`.

Inside of the outer `twitoff-DS##` folder create a new pipenv virtual environment and install the following packages:

- `flask` Flask is our Python-based web development framework that will help us serve up web pages, and build an API to interact with a SQLite database and a machine learning model.

- `jinja2` Jinja2 is a tool that will allow us to insert values (text mostly) into the HTML of a web page before sending that HTML back to the browser. This functionality is sometimes called "templating" and will help us change the contents of the web page based on how the user is interacting with it.

- `flask-sqlalchemy` SQLAlchemy is a tool for querying a SQL database with *Pytgon*. SQLAlchemy allows us to write Python and then will translate that python into SQL queries and database schema for us --kind of like how pymongo gave us Python functionality for interacting with the Mongo Database last week.

After installing these packages, activate your virtual environment, and then create three new files inside of the `twitoff` folder:

- `__init__.py` Just like in our Python packages, this init file will be the first thing that is run whenever we launch our app.
- `app.py` This is the most important file in the app. This is where we will create our `app` object and use it to detect when users are accessing specific pages and serve up HTML when they visit them.
- `models.py` This page is where we will create our database schema (model) and create the tables that the database needs to store User data and Tweet data. SQLAlchemy will let us use Python classes to define our database schemas, which is pretty convenient!

Inside of the `twitoff` folder make a new folder called `templates` this will hold the main frontend html file that our app presents to users. Inside of this folder create a file called `base.html` I'll give you the HTML to put into this file in Slack during the Guided Project. Remember, you don't need to understand all of the HTML and CSS for this project. That's frontend stuff. You *might* be how jinja2 works within our HTML files, but I won't expect you to know how to write any HTML by the end of this sprint.

## A Minimal Application

Let's start off by using the ["minimal application" provided to us in the Flask Docs](https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application) and let's understand what Flask is doing for us in the simplest version of an app that we can make.

Include the following code in your `app.py` file

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```

Then, from the Command Line in your outer `twitoff-DS##` folder run the following two commands.

`export FLASK_APP=app`

and

`flask run`

You should see a message about your app running on a development server along with the a messaget that the app is running on a url:

```bash
 * Running on http://127.0.0.1:5000/
```

In your browser visit `http://127.0.0.1:5000/` and you should see "Hello, World!" displayed as a web page in your browser.

You can also replace the `http://127.0.0.1:` in the URL with `localhost:` I find that it's easier to type out that way. Try visiting `localhost:5000` and you'll see the same result.

Next, let's try adding a new page to our app, this time we'll dynamically insert some information into the html. Add the following ot your app.py

```python
app_title = "Twitoff DS##"

@app.route("/test")
def test():
    return f"<p>Another {app_title} page</p>"
```

Before these changes take effect, you'll need to close down the server and restart it. You can use `ctrl + c` to kill the server and then run the two commands again to restart it.

After restarting the server, navigate to `localhost:5000` to make sure the app is running. And then visit `localhost:5000/test` You should see the return statement of the second function serving up a new page at this new address.

## Adding a template

Instead of just loading a small string of HTML when a person visits a specific page, we would like the server to respond with a lot more than that, maybe an entire page of HTML that can dyamically change as the user interacts with the page. This is what Flask templates allow. In Flask templates not only can we include a lot of useful HTML, we can also "template in" Python variables using Jinja2 rather than using a python f string. Copy the following html and include paste it into the `base.html` file in the templates folder:

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
      {% endblock %}
    </article>
    <!-- <script src="https://cdn.jsdelivr.net/npm/umbrellajs"/> -->
  </body>

</html>
```

Let's modify our Hello World route for the home page to use the `base.html` template file. We'll also need to import the `render_template` function from `flask` to help us with this.

```python
from flask import Flask, render_template

@app.route('/')
def root():
    return render_template('base.html', title="Home")
```

Remember, you'll need to stop and restart the server for the changes to take effect.

## Simplify our app initialization command

It's kind of a pain to have to export our app and run it in two steps everytime we want to start it up. What if our app was initialized automatically every time we ran flask?

Let's change our app.py file by wrapping all of our routes in a `create_app()` function, and then we can call that `create_app()` function from our `__ini__.py` file that gets automatically run whenever the app starts up. We'll also add a couple more routes for fun.

```python
from flask import Flask, render_template

def create_app():

    # Initilaize our app
    app = Flask(__name__)

    # Create a new "route" that detects when a user accesses it.
    # We'll attatch each route to our `app` object.
    @app.route('/')
    def root():
        # return page contents
        return render_template('base.html', title="Home")

    app_title = "Twitoff DS32"

    @app.route("/test")
    def test():
        return f"<p>Another {app_title} page</p>"

    @app.route('/hola')
    def hola():
        return "Hola, Twitoff!"

    # return our app object after attaching the routes to it.
    return app
```

In the `__init__.py` file add the following code so that the app starts up automatically.

```python
"""The first file that is run when running the twitoff package"""
from .app import create_app

APP = create_app()
```

Now we can run the app with the single command `flask run` in the command line to start up the app.

## Creating Database models (schema) with SQLAlchemy

No that we've got our web server creating some basic pages, let's do a little bit of database setup. In the `models.py` file add the following code. This is the most complex code that we'll write today and is a big part of what I want you to focus on understanding as part of your assignment this afternoon.

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

    def __repr__(self):
        return "<User: {}>".format(self.name)


class Tweet(DB.Model):
    """Keeps track of Tweets for each user"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))  # allows for text and links
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)
```

## Create some test Users and Tweets

When we want to interact with the database as if it was in a production environment, we need to start up our flask app using a slightly different command.

`FLASK_APP=app flask shell`

This will start up a REPL that we can use to create users and tweets.

`>>> from twitoff.models import User`

Because of SQLAlchemy's class structure, we can now create users and tweets in the database simply by instantiating objects using the `User` and `Tweet` classes.

`>>> user1 = User(id=1, username="Ryan")`

To create a tweet we'll need both the User class and the Tweet class since a Tweet needs a reference to a User as part of its schema.

`>>> from twitoff.models import User, Tweet`

Create a new user and a tweet that pertains to that user.

`>>> ryan = User(id=1, username="Ryan")`

`>>> tweet = Tweet(id=1, text="this is a tweet", user=ryan)`

Confirm that the user and tweet objects print out according to how we indicated they should in their respective `__repr__()` functions.

`>>> ryan`

`>>> tweet`

Confirm that the tweet and user objects have the attributes that we indicated.

`>>> ryan.username`

`>>> tweet.text`

Confirm that a relationship exists between the user and tweet objects. The user object now contains a list of tweets and each of those tweets is associated with a user.

`>>> tweet.user`

`>>> ryan.tweets`

`>>> tweet.user.tweets`

## Connect our database to our app

Now that our database models are created and are working properly, let's make sure that our app has access to our database. We'll need to import our database into our app.py. We'll also set up a couple of small configurations for the database within our create_app() function.

We will also add two new routes, one for resetting all users in the database so that the database is blank and a second one for populating the database with users. These functions will run whenever we visit their routes so we'll execute them by navigating to their respective pages.

```python
from re import DEBUG
from flask import Flask, render_template
from .models import DB, User, Tweet

def create_app():

    # Initilaize our app
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    # Create a new "route" that detects when a user accesses it.
    # We'll attatch each route to our `app` object.
    @app.route('/')
    def root():
        # return page contents
        return render_template('base.html', title="Home")

    app_title = "Twitoff DS32"

    @app.route("/test")
    def test():
        return f"<p>Another {app_title} page</p>"

    @app.route('/hola')
    def hola():
        return "hola, Twitoff"

    @app.route('/salut')
    def salut():
        return "salut, Twitoff"

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return '''The database has been reset. 
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset</a>
        <a href='/populate'>Go to populate</a>'''

    @app.route('/populate')
    def populate():
        ryan = User(id=1, username='ryan')
        DB.session.add(ryan)
        julian = User(id=2, username='julian')
        DB.session.add(julian)
        tweet1 = Tweet(id=1, text='tweet text', user=ryan)
        DB.session.add(tweet1)
        DB.session.commit()
        return '''Created some users. 
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset</a>
        <a href='/populate'>Go to populate</a>'''

    # return our app object after attaching the routes to it.
    return app 
```

Your app may crash until you run the `/reset` route for the first time. The reset route drops all of the information in the DB, but it also creates the `db.sqlite3` file. If you don't have that file already you'll need to access the `/reset` route in order to create it. Once it has been created initially you won't need to ever create the db file again (unless you manually delete it), so you should only ever need to do this step one time.

In the return statements of the new `/reset` and `/populate` routes I've added some HTML links so that we can easily navigate between the pages. The Home page already has a button that points to the reset database route. Adding the HTML for those links is totally optional but I find that it makes it easier to just click on the links to navigate around.

## Get users to show on the home page

Finally now that we can populate and erase our database at a whim, lets make it so that the users that exist in the database show up on the home page.

We'll need to change our home `'/'` route so that it queries the DB for users and then we'll need to pass those users in as a parameter to the `render_template()` function so that Jinja2 has access to those user variables

```python
@app.route('/')
    def root():
        # return page contents
        users = User.query.all()
        return render_template('base.html', title="Home", users=users)
```

Last of all, we'll add a for loop to our `base.html` file so that new pieces of html get added to the page for each user. Change the `<article> stuff in here</article>` section to look like the following:

```html
<article class="flex two" style="padding: 3em 1em;">
      {% block content %}
        {% for user in users %}
        <p>{{ user.username }}</p>
        {% endfor %}
      {% endblock %}
    </article>
```

After you've added that for loop restart your app, reset and populate your database and see if you can see database usernames being displayed on the home page. What you're seing there is the result of a full-stack web app that's detecting the route the user is visiting, querying the database, and then inserting the queried data into the HTML that the server is returning to the browser. Pretty Cool!
