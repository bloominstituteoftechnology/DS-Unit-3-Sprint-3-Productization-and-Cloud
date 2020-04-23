# The init file indicates that the folder lives inside is like a python module 
# and facilitates the importing of certain files within that module within that directory.
# The other role that it plays, is it's the entry point. It's the first place to look into that module directory

# Imports
from flask import Flask


from web_app.routes.home_routes import home_routes
from web_app.routes.book_routes import book_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)