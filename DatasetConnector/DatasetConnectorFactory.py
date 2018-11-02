from config import ConfigManager
from DatasetConnector import CSV as Csv, MySQL as Sql, Mongo as Mongo


class DatasetConnectorFactory(object):

    def __init__(self):
        pass

    def dataset(self,db_params):
        if ConfigManager.connector_list.get(db_params["name"]) == 'CSV':
            dataset = Csv.CSV().dataset(db_params)
        elif ConfigManager.connector_list.get(db_params["name"]) == 'SQL':
            dataset = Sql.MySQL().dataset(db_params)
        elif ConfigManager.connector_list.get(db_params["name"]) == 'MONGO':
            dataset = Mongo.Mongo().dataset(db_params)
        # elif Constants.algo_list.get(connectorSelect) == 'CASSANDRA':
        #     DatasetConnector = RF.RandomForest()
        # elif Constants.algo_list.get(connectorSelect) == 'EXCEL':
        #     DatasetConnector = SVM.SupportVectorMachine()
        return dataset

    def check_connection(self,db_params):
        status = False
        if ConfigManager.connector_list.get(db_params["name"]) == 'CSV':
            status = Csv.CSV().check_connection(db_params)
        elif ConfigManager.connector_list.get(db_params["name"]) == 'SQL':
            status = Sql.MySQL().check_connection(db_params)
        elif ConfigManager.connector_list.get(db_params["name"]) == 'MONGO':
            status = Mongo.Mongo().check_connection(db_params)
        # elif Constants.algo_list.get(connectorSelect) == 'CASSANDRA':
        #     DatasetConnector = RF.RandomForest()
        # elif Constants.algo_list.get(connectorSelect) == 'EXCEL':
        #     DatasetConnector = SVM.SupportVectorMachine()
        return status

    def get_column_list(self, db_params):
        column_list = None
        if ConfigManager.connector_list.get(db_params["name"]) == 'CSV':
            column_list = None
        elif ConfigManager.connector_list.get(db_params["name"]) == 'SQL':
            column_list = Sql.MySQL().get_columns(db_params)
        elif ConfigManager.connector_list.get(db_params["name"]) == 'MONGO':
            column_list = Mongo.Mongo().get_columns(db_params)
        # elif Constants.algo_list.get(connectorSelect) == 'CASSANDRA':
        #     DatasetConnector = RF.RandomForest()
        # elif Constants.algo_list.get(connectorSelect) == 'EXCEL':
        #     DatasetConnector = SVM.SupportVectorMachine()
        return column_list
