import pickle
import logging
from datetime import datetime
from logs import LogHandler
from data import ModelProcessor as mp
import os
from config import ConfigManager
import tensorflow as tf
ErrorLogger = logging.getLogger("ErrorLogs")
InfoLogger = logging.getLogger("InfoLogs")
LogHandler.setup_logging()

class LoadModelService(object):

    load_model_dict = {}

    def __init__(self):
        pass

    def load_model(self, load_model_params):
            status = dict()

            try:
                # model file name
                Directory = ConfigManager.ROOT_DIR + "/TrainedModelsDirectory"
                filename = str(load_model_params["modelName"]) + "_" + str(load_model_params["algorithm"]["name"]) + "_" \
                           + str(load_model_params["appId"]) + ".sav"
                filepath = os.path.join(Directory, filename)

                # load the model into memory from disk
                LoadModelService.load_model_dict[filename] = pickle.load(open(filepath, 'rb'))

                # update status in mongo
                status["loaded"] = True
                status["loadDate"] = str(datetime.utcnow())
                mp.ModelProcessor().update_key_mongo(load_model_params["appId"], load_model_params["modelName"], status)

            except Exception as e:
                ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up', 500)
                status["loaded"] = False
                status["loadDate"] = str(datetime.utcnow())
                status["loadErrorMessage"] = str(e)
                mp.ModelProcessor().update_key_mongo(load_model_params["appId"], load_model_params["modelName"], status)



    def check_if_model_load(self, load_model_params):

            # model file name
            filename = str(load_model_params["modelName"]) + "_" + str(load_model_params["algorithm"]["name"]) \
                            + "_" + str(load_model_params["appId"]) + ".sav"

            if filename in LoadModelService.load_model_dict:
                if LoadModelService.load_model_dict[filename] is not None:
                    return True

            return False

    def unload_model(self, load_model_params):

        # model file name
        filename = str(load_model_params["modelName"]) + "_" + str(load_model_params["algorithm"]["name"]) + "_" + str(
                    load_model_params["appId"])
        # delete the model from memory
        if filename in LoadModelService.load_model_dict:
            del LoadModelService.load_model_dict[filename]
            return True

        return False
