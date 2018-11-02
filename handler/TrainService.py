from data import DataPreProcessor as dp, ModelProcessor as mp
from Algorithms import AlgorithmFactory as AF
from DatasetConnector import DatasetConnectorFactory as DCF
from sklearn.model_selection import train_test_split
from config import ConfigManager
from datetime import datetime
from CustomException import CustomException as CE
import logging.config
from logs import LogHandler


ErrorLogger = logging.getLogger("ErrorLogs")
DebugLogger = logging.getLogger("DebugLogs")
InfoLogger = logging.getLogger("InfoLogs")
LogHandler.setup_logging()


class TrainService(object):
    train_values = {}

    def __init__(self):
        pass

    def train_model(self, train_model_params):
        split_params = {}
        try:
                # update status in mongo
                train_model_params["creationDate"] = str(datetime.utcnow())
                train_model_params["status"] = "InProgress"
                mp.ModelProcessor().save_model_mongo(train_model_params)

                # Fetch Dataset
                dataset = DCF.DatasetConnectorFactory().dataset(train_model_params["dbconnect"])

                # data preprocess & Data wrangling
                model_dict, dataset, feature_list, target_list = dp.DataPreProcessor().data_preprocess(train_model_params, dataset)

                # train test split
                features_train, features_test, target_train, target_test = \
                    train_test_split(dataset[feature_list], dataset[target_list], train_size=train_model_params["trainTest"])

                split_params["features_train"] = features_train
                split_params["features_test"] = features_test
                split_params["target_train"] = target_train
                split_params["target_test"] = target_test

                # train model
                selected_algorithm = model_dict["algorithm"]["name"]
                model_dict = AF.AlgorithmFactory().algorithm(selected_algorithm).train(split_params, model_dict)

                # update status in mongo
                model_dict["status"] = "Done"
                model_dict["completionDate"] = str(datetime.utcnow())
                mp.ModelProcessor().update_model_mongo(model_dict)
                print ("thread executed")

        except CE.DatasetConnectionFailed as e:
            ErrorLogger.exception('EXCEPTION %s: Bad Dataset connection Params "%s"', str(e.errors), str(e))
            train_model_params["status"] = "Error"
            print (str(e))
            train_model_params["ErrorMessage"] = str(e)
            train_model_params["completionDate"] = str(datetime.utcnow())
            mp.ModelProcessor().update_model_mongo(train_model_params)

        except Exception as e:
            ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up "%s"', 500, e.args)
            train_model_params["status"] = "Error"
            train_model_params["ErrorMessage"] = str(e.args[0])
            train_model_params["completionDate"] = str(datetime.utcnow())
            mp.ModelProcessor().update_model_mongo(train_model_params)
