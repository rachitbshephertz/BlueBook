from pymongo import MongoClient
from config import ConfigManager
from CustomException import CustomException as CE
import pymongo.errors


class Mongo(object):

    client = None

    def __init__(self):
        pass

    def connect(self):
        try:
            mongo_host = ConfigManager.mongo_prediction_analytics_host
            mongo_port = ConfigManager.mongo_prediction_analytics_port
            mongo_dbName = ConfigManager.mongo_prediction_analytics_dbName
            if not Mongo.client:
                Mongo.client = MongoClient(host=mongo_host, port=mongo_port, max_pool_size=None, waitQueueTimeoutMS=500)
            db = Mongo.client[mongo_dbName]

        except pymongo.errors.ConnectionFailure as e:
            raise Exception("Failed to establish connection with PredictionMongoDB : %s"
                                             % e.message, 504)
        except pymongo.errors.CollectionInvalid as e:
            raise Exception("Failed to establish connection with PredictionMongoDB : %s"
                            % e.message, 504)
        except pymongo.errors.ConfigurationError as e:
            raise Exception("Failed to establish connection with PredictionMongoDB : %s"
                            % e.message, 504)
        except Exception as e:
            raise Exception("Failed to establish connection with PredictionMongoDB : %s"
                            % e.message, 504)
        return db

