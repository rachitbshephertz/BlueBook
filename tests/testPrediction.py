import unittest
import json
from handler import PredictionController as pc
from handler import LoadModelService as LMS
from handler import PredictService as PR, TrainService as TR , ModelService as GMS


class testPrediction(unittest.TestCase):

    def testGetModelDetails(self):

        test_data = {
            "appId": "1",
            "modelName": "newdetnew",
            "features": ["{\"value\":\"S038\",\"columnName\":\"Center code\"}",
                         "{\"value\":\"P006\",\"columnName\":\"TestCode\"}"],
            "algorithm": {
                "name": "Naive Bayes",
                "type": "gaussianNB",
                "isDefault": True,
                "priors": "None"
            }
            }
        test_data = json.dumps(test_data)
        test_data = json.loads(test_data)

        LMS.LoadModelService().load_model(test_data)
        GMS.ModelService().delete_model(test_data)
        print(str(PR.PredictService().predict_service(test_data)))


if __name__ == '__main__':
    unittest.main()

