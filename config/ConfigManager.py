import configparser
import os
import sys

class Config():

    def __init__(self):
        pass

    @staticmethod
    def read_config():
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        config = configparser.RawConfigParser()
        configFilePath = os.path.join(os.path.split(ROOT_DIR)[0], 'config.properties')
        config.read(configFilePath)
        return config

config = Config.read_config()

ROOT_DIR = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

#MYSQLDatabase
hostname = config.get('MySQLDatabaseSection', 'database.hostname')
dbname = config.get('MySQLDatabaseSection', 'database.dbname')
username = config.get('MySQLDatabaseSection', 'database.user')
password = config.get('MySQLDatabaseSection', 'database.password')

#MongoDatabase
mongo_prediction_analytics_host = config.get('MongoDatabaseSection','mongo_prediction_analytics_host')
mongo_prediction_analytics_port = int(config.get('MongoDatabaseSection','mongo_prediction_analytics_port'))
mongo_prediction_analytics_dbName = config.get('MongoDatabaseSection','mongo_prediction_analytics_dbName')
model_collection = config.get('MongoDatabaseSection','model_collection')

# Algorithm Default Parameters Dict
random_forest_classifier_list = {
        "n_estimators": 10,
        "criterion": "gini",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "min_weight_fraction_leaf": 0.0,
        "max_features": "auto",
        "max_leaf_nodes": None,
        "min_impurity_decrease": 0.0,
        "min_impurity_split": None,
        "bootstrap": True,
        "oob_score": False,
        "n_jobs": 1,
        "verbose": 0,
        "random_state": None,
        "warm_start": False,
        "class_weight": None
}

naive_bayes_gaussianNB_list = {
        "priors": None
}

logistics_regression_list = {
        "penalty": 'l2',
        "dual": False,
        "tol": 1e-4,
        "C": 1.0,
        "fit_intercept": True,
        "intercept_scaling": 1,
        "class_weight": None,
        "random_state":None,
        "solver": 'liblinear',
        "max_iter": 100,
        "multi_class": 'ovr',
        "verbose": 0,
        "warm_start": False,
        "n_jobs": 1
}


algo_list = {
        "Logistics Regression": "LR",
        "Naive Bayes": "NB",
        "Neural Network": "NN",
        "Random Forest": "RF",
        "Support Vector Machine": "SVM"
}


connector_list = {
        "Sql Connect": "SQL",
        "Mongo Connect": "MONGO",
        "Cassandra Connect": "CASSANDRA",
        "CSV Connect": "CSV",
        "Excel Connect": "EXCEL",
}



#ERROR_CODE
error_code_400 = 400


#MONGO_QUERY
fetch_query_model = {"model_name":"$model_name"}