import json
from data import ModelProcessor as mp
from handler import LoadModelService as LMS
import logging.config
from CustomException import CustomException as CE
from logs import LogHandler
import numpy as np
from sklearn import preprocessing
import pickle
from config import ConfigManager
import os

ErrorLogger = logging.getLogger("ErrorLogs")
DebugLogger = logging.getLogger("DebugLogs")
InfoLogger = logging.getLogger("InfoLogs")
LogHandler.setup_logging()


class PredictService(object):

    def __init__(self):
        pass

    def predict_service(self, model_params):
        feature_dict = dict()
        feature_list = list()
        prediction_dict = dict()
        model_collection_data = mp.ModelProcessor().get_model_mongo_byAppIdandmodelName(model_params)

        if not len(model_params['features']) == len(model_collection_data["featureList"]):
            raise CE.InvalidPredictionParams("Invalid number of features, expected: "
                                             + str(len(model_collection_data["featureList"]))
                                             + " got: " + str(len(model_params['features'])), 403)

        # Add feature value to list and check if any categorical feature
        for feature in model_params["features"]:
            feature = json.loads(feature)
            if feature["value"]:
                if feature["columnName"] in model_collection_data["featureList"]:
                    if 'categoricalData' in model_collection_data:
                        if feature["columnName"] in model_collection_data["categoricalData"]:
                            if feature["value"] in model_collection_data["categoricalData"][feature["columnName"]]["encoding"]:
                                feature_dict[str(feature["columnName"])] = model_collection_data["categoricalData"][feature["columnName"]]["encoding"][feature["value"]]
                            else:
                                raise CE.InvalidPredictionParams("Model not trained for feature:" + feature["columnName"]
                                                             + " with value:" + str(feature["value"]), 403)
                        else:
                            if type(feature["value"]) == int or type(feature["value"])== float:
                                feature_dict[str(feature["columnName"])] = feature["value"]
                            else:
                                raise CE.InvalidPredictionParams("Model not trained for this feature:" + feature["columnName"]
                                                             + " to be categorical. Enter Int value", 403)
                    else:
                        if type(feature["value"]) == int or type(feature["value"]) == float:
                            feature_dict[str(feature["columnName"])] = feature["value"]
                        else:
                            raise CE.InvalidPredictionParams(
                                "Model not trained for this feature:" + feature["columnName"]
                                + " to be categorical. Enter Int value", 403)
                else:
                    raise CE.InvalidPredictionParams("Model not trained with feature: " + feature["columnName"], 403)
            else:
                raise CE.InvalidPredictionParams("Value can not be null for feature: " + feature["columnName"], 403)

        for feature in model_collection_data["featureList"]:
            feature_list.append(feature_dict[str(feature)])

        # scale data

        Directory = ConfigManager.ROOT_DIR + "/TrainedModelsDirectory"
        filename = str(model_params["modelName"]) + "_" + "minmaxScaler_" \
                       + str(model_params["appId"]) + ".sav"
        filepath = os.path.join(Directory, filename)

        min_max_scaler = pickle.load(open(filepath, 'rb'))
        feature_list = min_max_scaler.transform([feature_list])[0]

        # model file name
        if "Neural Network" in model_params["algorithm"]["name"]:
            filename = str(model_params["modelName"]) + "_" + str(model_params["algorithm"]["name"]) \
                       + "_" + str(model_params["appId"]) + ".hdf5"
        else:
            filename = str(model_params["modelName"]) + "_" + str(model_params["algorithm"]["name"]) \
                       + "_" + str(model_params["appId"]) + ".sav"

        # load the model from memory
        loaded_model = LMS.LoadModelService().load_model_dict[filename]

        # Make prediction
        if model_params["algorithm"]["name"] == 'Neural Network':
            feature_list = np.array([feature_list])
            from keras import backend
            with backend.get_session().graph.as_default() as g:
                prediction_list = loaded_model.predict_classes(feature_list)
            prediction_list = prediction_list[0]
        else:
            print("Something else")
            prediction_list = loaded_model.predict([feature_list])

        target_counter = 0

        for target in model_collection_data["targetList"]:
            if 'categoricalData' in model_collection_data:
                if target in model_collection_data["categoricalData"]:
                    cat_dict = dict(model_collection_data["categoricalData"][target]["encoding"])

                    cat_decoded_value = list(cat_dict.keys())[list(cat_dict.values()).index(prediction_list[target_counter])]
                    prediction_dict[str(target)] = str(cat_decoded_value)
                    target_counter = target_counter + 1
                else:
                    prediction_dict[str(target)] = prediction_list[target_counter]
                    target_counter = target_counter + 1
            else:
                    prediction_dict[str(target)] = prediction_list[target_counter]
                    target_counter = target_counter + 1

        return prediction_dict

    def predict_batch_service(self, model_params):
        predict_batch = []

        # model file name
        if "Neural Network" in model_params["algorithm"]["name"]:
            filename = str(model_params["modelName"]) + "_" + str(model_params["algorithm"]["name"]) \
                       + "_" + str(model_params["appId"]) + ".hdf5"
        else:
            filename = str(model_params["modelName"]) + "_" + str(model_params["algorithm"]["name"]) \
                       + "_" + str(model_params["appId"]) + ".sav"

        # load the model from memory
        loaded_model = LMS.LoadModelService().load_model_dict[filename]

        for batchFeature in model_params['batchFeatures']:
            print(batchFeature)

            model_params['features'] = batchFeature
            feature_dict = dict()
            feature_list = list()
            prediction_dict = dict()
            model_collection_data = mp.ModelProcessor().get_model_mongo_byAppIdandmodelName(model_params)

            if not len(model_params['features']) == len(model_collection_data["featureList"]):
                raise CE.InvalidPredictionParams("Invalid number of features, expected: "
                                                 + str(len(model_collection_data["featureList"]))
                                                 + " got: " + str(len(model_params['features'])), 403)

            # Add feature value to list and check if any categorical feature
            for feature in model_params["features"]:
                feature = json.loads(feature)
                if feature["value"]:
                    if feature["columnName"] in model_collection_data["featureList"]:
                        if 'categoricalData' in model_collection_data:
                            if feature["columnName"] in model_collection_data["categoricalData"]:
                                if feature["value"] in model_collection_data["categoricalData"][feature["columnName"]]["encoding"]:
                                    feature_dict[str(feature["columnName"])] = model_collection_data["categoricalData"][feature["columnName"]]["encoding"][feature["value"]]
                                else:
                                    raise CE.InvalidPredictionParams("Model not trained for feature:" + feature["columnName"]
                                                                 + " with value:" + str(feature["value"]), 403)
                            else:
                                if type(feature["value"]) == int or type(feature["value"])== float:
                                    feature_dict[str(feature["columnName"])] = feature["value"]
                                else:
                                    raise CE.InvalidPredictionParams("Model not trained for this feature:" + feature["columnName"]
                                                                 + " to be categorical. Enter Int value", 403)
                        else:
                            if type(feature["value"]) == int or type(feature["value"]) == float:
                                feature_dict[str(feature["columnName"])] = feature["value"]
                            else:
                                raise CE.InvalidPredictionParams(
                                    "Model not trained for this feature:" + feature["columnName"]
                                    + " to be categorical. Enter Int value", 403)
                    else:
                        raise CE.InvalidPredictionParams("Model not trained with feature: " + feature["columnName"], 403)
                else:
                    raise CE.InvalidPredictionParams("Value can not be null for feature: " + feature["columnName"], 403)

            for feature in model_collection_data["featureList"]:
                feature_list.append(feature_dict[str(feature)])

            # scale data as per original data
            Directory = ConfigManager.ROOT_DIR + "/TrainedModelsDirectory"
            filename = str(model_params["modelName"]) + "_" + "minmaxScaler_" \
                           + str(model_params["appId"]) + ".sav"
            filepath = os.path.join(Directory, filename)

            min_max_scaler = pickle.load(open(filepath, 'rb'))
            feature_list = min_max_scaler.transform([feature_list])[0]

            # Make prediction
            if model_params["algorithm"]["name"] == 'Neural Network':
                feature_list = np.array([feature_list])
                from keras import backend
                with backend.get_session().graph.as_default() as g:
                    prediction_list = loaded_model.predict_classes(feature_list)
                prediction_list = prediction_list[0]
            else:
                print("Something else")
                prediction_list = loaded_model.predict([feature_list])

            target_counter = 0

            for target in model_collection_data["targetList"]:
                if 'categoricalData' in model_collection_data:
                    if target in model_collection_data["categoricalData"]:
                        cat_dict = dict(model_collection_data["categoricalData"][target]["encoding"])

                        cat_decoded_value = list(cat_dict.keys())[list(cat_dict.values()).index(prediction_list[target_counter])]
                        prediction_dict[str(target)] = str(cat_decoded_value)
                        target_counter = target_counter + 1
                    else:
                        prediction_dict[str(target)] = prediction_list[target_counter]
                        target_counter = target_counter + 1
                else:
                        prediction_dict[str(target)] = prediction_list[target_counter]
                        target_counter = target_counter + 1

            predict_batch.append(prediction_dict)
        return predict_batch
