from flask import Flask, render_template

#creates Flask web server
app = Flask(__name__)

#default route

@app.route("/")
def template():
    return render_template("template.html")

@app.route("/home")
#available at default route
def home():
    return render_template("home.html") 

#another route
@app.route("/about")

def preds():
    return render_template("about.html")
    
if __name__ == "__main__":
    app.run(debug=True)

