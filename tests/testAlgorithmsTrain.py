import unittest
from handler import PredictionController as pc
import json
from flask import Flask, render_template, request,jsonify,json,g
from flask import Flask, current_app

class TestAlgorithms(unittest.TestCase):
    def testNaiveBayes(self):

        test_data = {
        "appId": "132",
        "modelName": "newdetnew",
        "creationDate": "",
        "trainTest": 80,
        "algorithm": {
                        "name": "Naive Bayes",
                        "type": "gaussianNB",
                        "isDefault": True,
                        "priors": "None"
                    },
        "dbconnect": {
                        "name": "CSV Connect",
                        "source": "https://apiindiablob.blob.core.windows.net/274-d9086e02f8ee9d46b719e18/dataset.csv"
                     },
        "features": ["{\"operation\":\"drop_row\",\"columnName\":\"Center code\"}", "{\"operation\":\"drop_row\",\"columnName\":\"TestCode\"}"],
        "targets": ["{\"operation\":\"mean\",\"columnName\":\"TOTAL TAT\"}"],
        "status": "",
        "accuracy": "",
        "updatedDate": "",
        "graphURL": ""
        }
        test_data = json.dumps(test_data)
        test_data = json.loads(test_data)
        pc.PredictionController().train_model((test_data))

if __name__ == '__main__':
    unittest.main()
