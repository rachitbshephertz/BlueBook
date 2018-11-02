from DatasetConnector import PredictionMongo as M
from config import ConfigManager


class ModelProcessor(object):

    def __init__(self):
        pass

    def get_model_mongo_byAppId(self, model_params):
        db = M.Mongo().connect()
        collection = db[ConfigManager.model_collection]
        model_Cursor = collection.find({"appId": model_params['appId']})
        return model_Cursor

    def get_model_mongo_byAppId_count(self, model_params):
        db = M.Mongo().connect()
        collection = db[ConfigManager.model_collection]
        model_json = collection.find({"appId": model_params['appId']})
        return model_json.count()

    def get_model_mongo_byAppIdandmodelName(self, model_params):
        db = M.Mongo().connect()
        collection = db[ConfigManager.model_collection]
        model_json = collection.find_one({"appId": model_params['appId'], "modelName": model_params['modelName']})
        return model_json

    def get_model_mongo_byAppIdandmodelName_count(self, model_params):
        db = M.Mongo().connect()
        collection = db[ConfigManager.model_collection]
        model_json = collection.find({"appId": model_params['appId'], "modelName": model_params['modelName']})
        return model_json.count()

    def update_model_mongo(self, json):
        db = M.Mongo().connect()
        collection = db[ConfigManager.model_collection]
        collection.update({"appId": json["appId"], "modelName": json["modelName"]}, json)

    def update_key_mongo(self, appId, modelName, status):
        db = M.Mongo().connect()
        collection = db[ConfigManager.model_collection]
        collection.update({"appId": appId, "modelName": modelName}, {"$set": status}, True)

    def delete_model_mongo(self, json):
        db = M.Mongo().connect()
        collection = db[ConfigManager.model_collection]
        status = collection.remove({"appId": json["appId"], "modelName": json["modelName"]})
        return status

    def save_model_mongo(self, json):
        db = M.Mongo().connect()
        collection = db[ConfigManager.model_collection]
        collection.insert(json)
