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
with open('model.pkl', 'r') as picklefile:
    model = pickle.load(picklefile)

@app.route('/')
def hello_world():
    logger.debug('Default route')
    return app.send_static_file('sales.html')


@app.route('/predict', methods=['GET'])
def predict_stuff():
    logger.debug('Predict route called')

    Store = request.args['Store']
    Dept = request.args['Dept']
    week = request.args['week']

    logger.debug('Received the following params:' + str(Store) + ' and ' + str(Dept) + ' and ' + str(week))

    item = [int(Store), int(Dept), int(week)]
    logger.debug(json.dumps(item))
    sales = float(model.predict(item))
    logger.debug(json.dumps(sales))

    results = {'Weekly Sales': sales}
    # item = [pclass, sex, age, fare, sibsp]
    # score = PREDICTOR.predict_proba(item)
    # results = {'survival chances': score[0,1], 'death chances': score[0,0]}
    # return flask.jsonify(results)

    # my_dict = {'Store': Store, 'Department': Dept, 'week': week, 'holiday': holiday}

    return json.dumps(results)

if __name__ == '__main__':

    HOST = '127.0.0.1'
    PORT = '4000'

    app.run(HOST, PORT)
    app.run(debug=True)