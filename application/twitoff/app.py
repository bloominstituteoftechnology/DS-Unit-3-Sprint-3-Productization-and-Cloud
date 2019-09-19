"""Main app/routing file for TwitOff."""
from decouple import config
from flask import Flask, render_template, request
from .models import DB, User
from .createtables import Create
from .predict import predict_user
from .twitter import add_or_update_user, update_all_users


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    # Create route to the home page
    @app.route('/')
    def root():
        DB.create_all()
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    # Create routes to add and retrieve Twitter users
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = 'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, messgae=message)

    # Create route to display which user is most likely to tweet the fake tweet
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'], request.values['user2']])

        if user1 == user2:
            return 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1, user2, request.values['tweet_text'])
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1)
            return render_template('prediction.html', title='Prediction', message=message)

    # Create route to allow user to reset the database
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset!', users=[])

    # Create route to allow user to pull most recent tweets
    @app.route('/update')
    def update():
        update_all_users()
        return render_template('base.html', users=User.query.all(),
                               title='Tweets have been updated!')

    return app