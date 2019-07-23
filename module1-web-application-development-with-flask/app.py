from flask import Flask, render_template

#create flask web server
app = Flask(__name__)

#routes determine location
# default route is 
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/predictions")
def preds():
    return "make preds"


if __name__ == '__main__':
    app.run(debug=True)