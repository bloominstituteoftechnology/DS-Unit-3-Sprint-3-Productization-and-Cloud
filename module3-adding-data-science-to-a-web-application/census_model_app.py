import numpy as np
from flask import Flask, abort, jsonify, request
import pickle

my_model = pickle.load(open('census_income_model.pkl', 'rb'))

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def make_predict():
    data = request.get_json(force=True)
    predict_request = [data['Service'], data['Production'],
                       data['Unemployment'], data['MeanCommute'],
                       data['Poverty'], data['Professional']]
    predict_request = np.array(predict_request).reshape(1, -1)
    y_hat = my_model.predict(predict_request)
    output = {'y_hat': int(y_hat[0])}
    return jsonify(results=output)


if __name__ == '__main__':
    app.run(port=9000, debug=True)