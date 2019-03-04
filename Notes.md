
#### Day 1
1. Create a new repo with python .gitignore, MIT License, and Readme.md
2. Clone repo locally, `cd` into the repo directory.
3. Make sure to have `pipenv` installed, run `which pipenv`, if nothing appears - run `brew install pipenv` or other similar command.
4. Run `pipenv install Flask`. It should output `Pipefile` and `Pipefile.lock` files in the root of the repo directory.
5. Run `pipenv shell` , and the current repo directory name should appear in the name of environment in a shell.
6. Open the repo in editor by running `subl .`, `code .`, or similar.
7. Add file `hello.py` and inside the file, add 

  ```from flask import Flask
   app = Flask(__name__)

   @app.route("/")
   def hello():
       return "Hello World!"
  ``` 
     
8. In the shell, run `FLASK_APP=hello.py flask run`. This command should spin the flask server and open in browser localhost outputted in the shell with the phrase `Hello World!` written previously in `hello.py` file. By doing so, we've checked the server is up and running and after we don't need `hello.py` file. Run `rm hello.py` to delete the file.
9. Run 
 `mkdir twitoff`, 
 `cd twitoff`, 
 `touch __init__.py app.py` 
 to create twitoff directory and `__init__.py` and `app.py` files in it.
 
10. In `__init__.py` file, add:

  ```from .app import create_app
     APP = create_app()
   ```
 
   to make the file an entry point for TwitOff Flask application.
 
11. In `app.py` file add:

  ```from flask import Flask

   def create_app():
      app = Flask(__name__)

       @app.route("/")
      def root():
          return "Welcome to TwitOff!"

       return app
```
 to create and configure an instance of the Flask application.
 
12. In the shell, to stop the server spinned previously, run `Ctrl + C`.

13. To run the instance of Flask application, in the shell run

```FLASK_APP=twitoff:APP flask run```

which should spin new Flask server and output `Welcome to TwitOff!` in the localhost in browser. Stop the server by running `Ctrl + C`.

14. To add `SQLAlchemy` database to the app, run `pipenv install flask-sqlalchemy` in the root directory of the app.

15. In the `twitoff` directory, run `touch models.py`, and in `models.py`, add the following: 

```from flask_sqlalchemy import SQLAlchemy

 DB = SQLAlchemy()


 class User(DB.Model):
    """Twitter users that we pull and analyze Tweets for."""
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)

     def __repr__(self):
        return '<User {}>'.format(self.name)

 class Tweet(DB.Model):
    """Tweets."""
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280))
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

     def __repr__(self):
        return '<Tweet {}>'.format(self.text)
```
to create SQLAlchemy models for TwitOff.

16. In `app.py` file, add `from .models import DB` and inside the `create_app` function add

``` 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)
```
 
 so that the final file looks like this:
```
  from flask import Flask
  from .models import DB


  def create_app():
      """Create and configure an instance of the Flask application."""
      app = Flask(__name__)
      app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
      DB.init_app(app)

      @app.route('/')
      def root():
          return 'Welcome to TwitOff!'

      return app
 ```
 Now app is ready!

17. To check if app is functional, and in order to manipulate the DB, in the shell, run 

```
FLASK_APP=twitoff:APP flask shell
```
then run `DB` - this should output the following:

```
<SQLAlchemy engine=sqlite:////Users/[YOUR_USER_NAME]/Desktop/TwitOff/twitoff/db.sqlite3>
```

18. There are 2 tables - Users and Tweets. These are the commands to add users and tweets:

  we should import the models to manipulate the DB:
  ```
  from twitoff.models import *
  ``` 
   
  add a user with username elonmusk:
  ```
  u1 = User(name='elonmusk')
  ``` 

  add a tweet:
  ```
  t1 = Tweet(text='Stop censoring science! https://t.co/R4XEtymtnH')
  ``` 
  append t1 tweet to user u1:
  ```
  u1.tweets.append(t1)
  ```
  
  add both to the DB session:

  ```
  DB.session.add(u1)
  ```

  ```
  DB.session.add(t1)
  ```  
  
  add to save in the DB:
  ```
  DB.session.commit()
  ``` 


  
