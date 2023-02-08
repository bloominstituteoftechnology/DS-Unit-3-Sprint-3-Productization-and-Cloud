# Web Application Development with Flask

In the modern day, most applications we interact with are *web* applications -
client-server architectures delivered via HTTP and accessed with a web browser.
As a data scientist we will generally not build such applications, but we do
have to *understand* them and their components.

## Learning Objectives

- Distinguish between front-end, back-end, database, and what tasks are
  appropriate for which
- Create a simple Python web application that exposes an API to URL endpoints

## Before Lecture

If you haven't already, complete the SSH key setup instructions for [adding an SSH key to your local machine](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and also [adding that same SSH key to your GitHub profile](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) so that you can push and pull repositories to GitHub using SSH as the connection/authentication method. If you do this, you'll be able to more directly follow along with any Git/GitHub related portions of our guided projects. 

Read up on [Flask](http://flask.pocoo.org/), a "microframework" for developing
web applications. All this really means is that it's small and modular, and
mostly just provides for URL routing and responses - for other things
(templates, database, forms) you pick and choose your own other packages (and
we'll give you some specific choices for this sprint).

Flask is not as fully featured as a development framework as other Python web development frameworks (like Django for example). However, its simplicity lets us build an app by writing code that is closer to vanilla Python. Because the framework's doing less work for us, there's less about how the framework works that we'll have to learn --And even then, there will still be a whole lot to learn.

If you're interested in getting into web development with Python with bigger and more serious projects (for example if you need user authentication where people can log in, and log out) then I would recommend looking into Django. You'll see a lot of similarities between Django and Flask, but Django has a more sophisticated set of features for building big web applications.

## Guided Project Task

See [guided-project.md](https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud/blob/master/module1-web-application-development-with-flask/guided-project.md)

## Assignment

See [assignment.md](https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud/blob/master/module1-web-application-development-with-flask/assignment.md)

## Resources and Stretch Goals

- [Jinja2](http://jinja.pocoo.org/) is the dominant template engine, which you
  will use to build the look and layout of the pages in your application
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) is an ORM
  (object-relational mapping), and will let us both (a) not have to write SQL,
  and (b) use OOP to interact with data with multiple backends (SQLite locally,
  and PostgreSQL in the cloud)
- [SQLAlchemy Data Types](https://docs.sqlalchemy.org/en/latest/core/type_basics.html) are needed
  to build usable models that will translate to SQL
- Making the front-end look nice is very much a stretch goal throughout this
  sprint - but if you are interested in it, [Picnic CSS](https://picnicss.com/)
  and [Umbrella JS](https://umbrellajs.com/) are nice lightweight and modern
  tools (alternatives to Bootstrap and JQuery respectively)
- Experiment with SQLAlchemy models - you can add more fields of interest to the
  `Tweet` and `User` models and/or add different models for other purposes
