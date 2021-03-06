import pickle
import ast, os
import numpy as np
import logging.config
from logs import LogHandler
from sklearn import preprocessing
from config import ConfigManager
from DatasetConnector import DatasetConnectorFactory as DCF

ErrorLogger = logging.getLogger("ErrorLogs")
DebugLogger = logging.getLogger("DebugLogs")
InfoLogger = logging.getLogger("InfoLogs")
LogHandler.setup_logging()


class DataPreProcessor(object):

    def __init__(self):

        pass

    def data_preprocess(self, model_dict, dataset):

        try:

            feature_list = self.get_feature_list(model_dict)
            model_dict["featureList"] = feature_list
            target_list = self.get_target_list(model_dict)
            model_dict["targetList"] = target_list
            print (dataset.head())

            # replace ? with NAN for handling later
            dataset = dataset.replace('?', np.NaN)
            dataset = dataset.replace(' ?', np.NaN)

            # Drop duplicate rows from dataset
            dataset = dataset.drop_duplicates()

            # Handle Missing values
            dataset = self.handle_missing_values(model_dict, dataset)

            # Handle Categorical(string) data by converting to int
            model_dict, dataset = self.handle_catagorical_data(model_dict, dataset)

            # Scale feature list data
            dataset = self.scale_data(dataset,feature_list,model_dict)

            return model_dict, dataset, feature_list, target_list

        except Exception as e:
            ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up "%s"', 500, str(e))
            raise Exception("Failed to preProcess data: %s"
                                             % str(e), 500)

    def scale_data(self, dataset, feature_list, model_dict):
        min_max_scaler = preprocessing.MinMaxScaler()
        dataset[feature_list] = min_max_scaler.fit_transform(dataset[feature_list])

        # save the minmax scaler to disk
        Directory = ConfigManager.ROOT_DIR + "/TrainedModelsDirectory"
        filename = str(model_dict["modelName"]) + "_" + "minmaxScaler_" \
                   + str(model_dict["appId"]) + ".sav"
        filepath = os.path.join(Directory, filename)

        files = open(filepath, 'wb')
        pickle.dump(min_max_scaler, files, protocol=pickle.HIGHEST_PROTOCOL)
        files.close()

        return dataset

    def handle_catagorical_data(self, model_dict, dataset):
        categorical_data = {}
        count = 0

        for feature in model_dict["features"]:
            categorical_data_feature = {}
            categorical_mapping_feature = {}
            feature = ast.literal_eval(feature)
            feature_name = feature["columnName"]
            if dataset[feature_name].dtypes == 'object':
                count = count + 1

                from sklearn import preprocessing
                le = preprocessing.LabelEncoder()
                le.fit(dataset[feature_name])
                for i, x in zip(le.classes_, (le.transform(le.classes_))):
                    categorical_mapping_feature[i] = int(x)
                categorical_data_feature["encoding"] = categorical_mapping_feature
                categorical_data[feature_name] = categorical_data_feature
                dataset[feature_name] = le.fit_transform(dataset[feature_name])

        for target in model_dict["targets"]:
            categorical_data_target = {}
            categorical_mapping_target = {}
            target = ast.literal_eval(target)
            target_name = target["columnName"]
            if dataset[target_name].dtypes == 'object':
                count = count + 1
                from sklearn import preprocessing
                le = preprocessing.LabelEncoder()
                le.fit(dataset[target_name])
                for i, x in zip(le.classes_, (le.transform(le.classes_))):
                    categorical_mapping_target[i] = int(x)
                categorical_data_target["encoding"] = categorical_mapping_target
                categorical_data[target_name] = categorical_data_target
                dataset[target_name] = le.fit_transform(dataset[target_name])

        if count > 0:
            model_dict["categoricalDataExist"] = True
            model_dict["categoricalData"] = categorical_data

        return model_dict, dataset

    def handle_missing_values(self,model_dict, dataset):
        for feature in model_dict["features"]:
            feature = ast.literal_eval(feature)
            if dataset[feature["columnName"]].isnull().values.any():
                if feature["operation"] == 'mean':
                    dataset[feature["columnName"]].fillna(dataset[feature["columnName"]].mean(), inplace=True)
                if feature['operation'] == 'drop_row':
                    dataset = dataset[dataset[feature["columnName"]].notnull()]
                if feature["operation"] == 'min':
                    dataset[feature["columnName"]].fillna(dataset[feature["columnName"]].min(), inplace=True)
                if feature['operation'] == 'max':
                    dataset[feature["columnName"]].fillna(dataset[feature["columnName"]].max(), inplace=True)
                if feature['operation'] == 'forwardfill':
                    dataset[feature["columnName"]].fillna( method='ffill', inplace=True)
                if feature['operation'] == 'backwardfill':
                    dataset[feature["columnName"]].fillna( method='bfill', inplace=True)
                if feature['operation'] == 'max':
                    dataset[feature["columnName"]].fillna(dataset[feature["columnName"]].max(), inplace=True)

        for target in model_dict["targets"]:
            target = ast.literal_eval(target)
            if dataset[target["columnName"]].isnull().values.any():
                if target["operation"] == 'mean':
                    dataset[target["columnName"]].fillna(dataset[target["columnName"]].mean(), inplace=True)
                if target['operation'] == 'drop_row':
                    dataset = dataset[dataset[target["columnName"]].notnull()]
                if target["operation"] == 'min':
                    dataset[target["columnName"]].fillna(dataset[target["columnName"]].min(), inplace=True)
                if target['operation'] == 'max':
                    dataset[target["columnName"]].fillna(dataset[target["columnName"]].max(), inplace=True)
                if target['operation'] == 'forwardfill':
                    dataset[target["columnName"]].fillna(method='ffill', inplace=True)
                if target['operation'] == 'backwardfill':
                    dataset[target["columnName"]].fillna(method='bfill', inplace=True)
                if target['operation'] == 'max':
                    dataset[target["columnName"]].fillna(dataset[target["columnName"]].max(), inplace=True)
        return dataset

    def get_feature_list(self,model_dict):
        feature_list = []
        for feature in model_dict["features"]:
            feature = ast.literal_eval(feature)
            feature_name = feature["columnName"]
            feature_list.append(feature_name)
        return feature_list

    def get_target_list(self,model_dict):
        target_list = []
        for target in model_dict["targets"]:
            target = ast.literal_eval(target)
            target_name = target["columnName"]
            target_list.append(target_name)
        return target_list

    def best_feature_selection(self, model_dict):
        # Fetch Dataset
        dataset = DCF.DatasetConnectorFactory().dataset(model_dict["dbconnect"])

        # replace ? with NAN for handling later
        dataset = dataset.replace('?', np.NaN)
        dataset = dataset.replace(' ?', np.NaN)

        # Drop duplicate rows from dataset
        dataset = dataset.drop_duplicates()

        # Handle Missing values
        dataset = dataset.dropna()

        from sklearn.ensemble import ExtraTreesClassifier
        X = dataset[model_dict["featureList"]]
        Y = dataset[model_dict["targetList"]]

        # feature extraction
        model = ExtraTreesClassifier()
        model.fit(X, Y)
        listScore = model.feature_importances_
        featureScore = dict()
        for i in range(len(model_dict["featureList"])):
            print(model_dict["featureList"][i])
        for g in listScore:
            print(g)
        for i in range(len(model_dict["featureList"])):
            featureScore[model_dict["featureList"][i]]= listScore[i]
        return featureScore
