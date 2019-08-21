import pickle
import json
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request

MODEL_FILE = "iris_model2.pkl"
# model
iris_model = pickle.load(open(MODEL_FILE, 'rb'))

app = Flask(__name__)

@app.route("/api", methods=['POST'])
def make_predict():
    data = request.get_json(force=True)
    predict_request = [v for k, v in data.items()]
    predict_request = np.array(predict_request).reshape(1, -1)
    
    y_pred = iris_model.predict(predict_request)
    
    output = {'y_pred' : int(y_pred[0])}
    
    return jsonify(results=output)

@app.route("/score", methods=['POST'])
def model_score():
    data = request.get_json(force=True)
    print(data['X'], "\n\n")
    print(data['y'], "\n\n")
    X = pd.read_json(data['X'])
    y = pd.read_json(data['y'])
    print(X, y)
    #predict_request = [v for k, v in data.items()]
    #print(predict_request)
    #predict_request = np.array(predict_request).reshape(1, -1)
    #print(predict_request)
    score = iris_model.score(X, y)
    
    output = {'model_score' : int(score)}
    
    return jsonify(results=output)

    
if __name__ == "__main__":
    app.run(debug = True)