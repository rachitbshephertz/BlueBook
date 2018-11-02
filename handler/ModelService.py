from data import ModelProcessor as mp
import logging.config
from logs import LogHandler
from handler import LoadModelService as LMS
import os
from config import ConfigManager

ErrorLogger = logging.getLogger("ErrorLogs")
DebugLogger = logging.getLogger("DebugLogs")
InfoLogger = logging.getLogger("InfoLogs")
LogHandler.setup_logging()


class ModelService(object):

    def __init__(self):
        pass

    def get_all_model_details(self, model_params):
        all_models = list()
        try:
            collection_data = mp.ModelProcessor().get_model_mongo_byAppId(model_params)
            print ('\n All data from model Database by appId \n')
            for model in collection_data:
                model_values = {}
                if 'appId' in model:
                    if model['appId'] is not None:
                        model_values['appId'] = model['appId']
                if 'modelName' in model:
                    if model['modelName'] is not None:
                        model_values['modelName'] = model['modelName']
                if 'creationDate' in model:
                    if model['creationDate'] is not None:
                        model_values['creationDate'] = model['creationDate']
                if 'algorithm' in model:
                    if model['algorithm'] is not None:
                        model_values['algorithm'] = model['algorithm']
                if 'accuracy' in model:
                    if model['accuracy'] is not None:
                        model_values['accuracy'] = model['accuracy']
                if 'completionDate' in model:
                    if model['completionDate'] is not None:
                        model_values['completionDate'] = model['completionDate']
                if 'status' in model:
                    if model['status'] is not None:
                        model_values['status'] = model['status']
                if 'ErrorMessage' in model:
                    if model['ErrorMessage'] is not None:
                        model_values['ErrorMessage'] = model['ErrorMessage']
                if 'loaded' in model:
                    if model['loaded'] is not None:
                        model_values['deployed'] = model['loaded']
                if 'loadDate' in model:
                    if model['loadDate'] is not None:
                        model_values['loadDate'] = model['loadDate']

                all_models.append(model_values)

        except Exception as e:
                ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up', 500)
                raise Exception("Failed to get all model details: %s" % e.message, 500)

        return all_models

    def get_model_details(self, model_params):
        model_values = {}
        try:
            model = mp.ModelProcessor().get_model_mongo_byAppIdandmodelName(model_params)
            print ('\n  model Database by appId and model name\n')
            if 'appId' in model:
                if model['appId'] is not None:
                    model_values['appId'] = model['appId']
            if 'modelName' in model:
                if model['modelName'] is not None:
                    model_values['modelName'] = model['modelName']
            if 'creationDate' in model:
                if model['creationDate'] is not None:
                    model_values['creationDate'] = model['creationDate']
            if 'algorithm' in model:
                if model['algorithm'] is not None:
                    model_values['algorithm'] = model['algorithm']
            if 'accuracy' in model:
                if model['accuracy'] is not None:
                    model_values['accuracy'] = model['accuracy']
            if 'completionDate' in model:
                if model['completionDate'] is not None:
                    model_values['completionDate'] = model['completionDate']
            if 'status' in model:
                if model['status'] is not None:
                    model_values['status'] = model['status']
            if 'ErrorMessage' in model:
                if model['ErrorMessage'] is not None:
                    model_values['ErrorMessage'] = model['ErrorMessage']
            if 'loaded' in model:
                if model['loaded'] is not None:
                    model_values['deployed'] = model['loaded']
            if 'loadDate' in model:
                if model['loadDate'] is not None:
                    model_values['deployDate'] = model['loadDate']

        except Exception as e:
            ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up', 500)
            raise Exception("Failed to get all model details: %s" % str(e), 500)

        return model_values

    def delete_model(self, model_params):
        status = False
        Directory = ConfigManager.ROOT_DIR + "/TrainedModelsDirectory"
        filename = str(model_params["modelName"]) + "_" + str(model_params["algorithm"]["name"]) + "_" \
                   + str(model_params["appId"]) + ".sav"
        filepath = os.path.join(Directory, filename)

        try:
            result = mp.ModelProcessor().delete_model_mongo(model_params)
            if result["n"] >= 1:
                status = True

            if LMS.LoadModelService().check_if_model_load(model_params):
                status = LMS.LoadModelService().unload_model(model_params)

            # remove trained model file
            if os.path.isfile(filepath):
                os.remove(filepath)

        except Exception as e:
                ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up', 500)
                raise Exception("Failed to delete model: %s" % e.message, 500)

        return status
