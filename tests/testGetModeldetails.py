import unittest
import json
from handler import PredictionController as pc

class testGetModelDetails(unittest.TestCase):

    def testGetModelDetails(self):
        test_data = {
            "appId": "1"}
        test_data = json.dumps(test_data)
        test_data = json.loads(test_data)
        pc.PredictionController().get_model((test_data))


if __name__ == '__main__':
    unittest.main()