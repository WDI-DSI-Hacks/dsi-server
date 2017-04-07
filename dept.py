from flask import Flask
from flask import request
import logging
from logging.handlers import TimedRotatingFileHandler
import json


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = TimedRotatingFileHandler('test.log', when='d', interval=1, backupCount=3)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

app = Flask(__name__)

#-------- MODEL -----------#
import pickle
import numpy as np
import pandas as pd

with open('model.pkl', 'r') as picklefile:
    model = pickle.load(picklefile)

with open('test.pkl', 'r') as picklefile:
    test = pickle.load(picklefile)

with open('unemp.pkl', 'r') as picklefile:
    unemp = pickle.load(picklefile)

@app.route('/')
def hello_world():
    logger.debug('Default route')
    return app.send_static_file('sales.html')


@app.route('/predict', methods=['GET'])
def predict_stuff():
    logger.debug('Predict route called')

    Dept = request.args['Dept']
    week = 14
    Store = range(1,46)

    logger.debug('Received the following params:' + str(Dept) )


    forecast = []
    for i in Store:
        test.iloc[:,:] = 0.0
        test['s_' + str(i)] = 1
        test['d_' + str(Dept)] = 1
        test['w_' + str(week)] = 1
        test['Unemployment'] = float(unemp['Unemployment'][unemp['Store'] == int(i)])
        sales = float(model.predict(test))
        logger.debug(json.dumps(sales))
        forecast.append(sales)


    results = {'Weekly_Sales': forecast}
    # item = [pclass, sex, age, fare, sibsp]
    # score = PREDICTOR.predict_proba(item)
    # results = {'survival chances': score[0,1], 'death chances': score[0,0]}
    # return flask.jsonify(results)

    # my_dict = {'Store': Store, 'Department': Dept, 'week': week, 'holiday': holiday}

    return json.dumps(results)

if __name__ == '__main__':

    HOST = '127.0.0.1'
    PORT = '5000'

    app.run(HOST, PORT)
    app.run(debug=True)