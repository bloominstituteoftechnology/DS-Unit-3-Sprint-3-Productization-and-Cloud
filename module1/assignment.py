from flask import Flask, render_template

##this is the app flask web server
app = Flask(__name__)

#this is root of web server /index.html
@app.route('/')
##function has to go directly nuder this to be valid
def index():
    return 'Place HTMl code here'

##this is /contact
@app.route("/contact")
##function to be valid
def contact():
    return 'place HTML code or template here'

##set name = main to run app
if __name__ == '__main__':
    app.run(debug=True)