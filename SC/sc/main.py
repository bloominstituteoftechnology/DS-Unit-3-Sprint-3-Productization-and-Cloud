from flask import Flask
import openaq

def create_app():

    app = Flask(__name__)

    @app.route('/')
    def root():
        api = openaq.OpenAQ()

        status, resp = api.cities()
        return f'Status: {status}\nResp: {resp}'
    
    return app
