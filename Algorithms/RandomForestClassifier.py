import pickle
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier as RFC
import os
import ast
from config import ConfigManager


class RandomForestClassifier(object):

    def __init__(self):
        pass

    def train(self, split_params, model_dict):
        algo_parameters_dict = ConfigManager.random_forest_classifier_list
        Directory = ConfigManager.ROOT_DIR + "/TrainedModelsDirectory"
        filename = str(model_dict["modelName"]) + "_" + str(model_dict["algorithm"]["name"]) + "_" \
                                                + str(model_dict["appId"]) + ".sav"
        filepath = os.path.join(Directory, filename)
        isDefault = str(model_dict["algorithm"]["isDefault"])
        if 'False' in isDefault:
            for param in model_dict["algorithm"]["parameters"]["params"]:
                param = ast.literal_eval(param)
                if param["name"] in algo_parameters_dict:
                    if param["value"] is not None:
                        algo_parameters_dict[param["name"]] = param["value"]

        trained_model = RFC(n_estimators=algo_parameters_dict["n_estimators"],
                            criterion=algo_parameters_dict["criterion"],
                            max_depth=algo_parameters_dict["max_depth"],
                            min_samples_split=algo_parameters_dict["min_samples_split"],
                            min_samples_leaf=algo_parameters_dict["min_samples_leaf"],
                            min_weight_fraction_leaf=algo_parameters_dict["min_weight_fraction_leaf"],
                            max_features=algo_parameters_dict["max_features"],
                            max_leaf_nodes=algo_parameters_dict["max_leaf_nodes"],
                            min_impurity_decrease=algo_parameters_dict["min_impurity_decrease"],
                            min_impurity_split=algo_parameters_dict["min_impurity_split"],
                            bootstrap=algo_parameters_dict["bootstrap"],
                            oob_score=algo_parameters_dict["oob_score"],
                            n_jobs=algo_parameters_dict["n_jobs"],
                            random_state=algo_parameters_dict["random_state"],
                            verbose=algo_parameters_dict["verbose"],
                            warm_start=algo_parameters_dict["warm_start"],
                            class_weight=algo_parameters_dict["class_weight"])

        trained_model.fit(split_params["features_train"], split_params["target_train"])

        # save the model to disk
        files = open(filepath, 'wb')
        pickle.dump(trained_model, files, protocol=pickle.HIGHEST_PROTOCOL)
        files.close()
        predict = trained_model.predict(split_params["features_test"])
        accuracy = accuracy_score(split_params["target_test"], predict)
        model_dict["accuracy"] = accuracy
        model_dict["actual"] = list(split_params["target_test"])
        model_dict["predicted"] = list(map(int, predict))
        return model_dict

