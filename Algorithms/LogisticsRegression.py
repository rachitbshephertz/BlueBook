import pickle
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression as LR
import os
import ast
from config import ConfigManager


class LogisticsRegression(object):

    def __init__(self):
        pass

    def train(self, split_params, model_dict):
        algoithm_parameters_dict = ConfigManager.logistics_regression_list
        Directory = ConfigManager.ROOT_DIR + "/TrainedModelsDirectory"
        filename = str(model_dict["modelName"]) + "_" + str(model_dict["algorithm"]["name"]) + "_" \
                   + str(model_dict["appId"]) + ".sav"
        filepath = os.path.join(Directory, filename)

        if not bool(model_dict["algorithm"]["isDefault"]):
            for param in model_dict["algorithm"]["parameters"]:
                param = ast.literal_eval(param)
                if param["name"] in algoithm_parameters_dict:
                    if param["value"] is not None:
                        algoithm_parameters_dict[param["name"]] = param["value"]

        trained_model = LR(penalty=algoithm_parameters_dict["penalty"],
                           dual=algoithm_parameters_dict["dual"],
                           tol=algoithm_parameters_dict["tol"],
                           C=algoithm_parameters_dict["C"],
                           fit_intercept=algoithm_parameters_dict["fit_intercept"],
                           intercept_scaling=algoithm_parameters_dict["intercept_scaling"],
                           class_weight=algoithm_parameters_dict["class_weight"],
                           random_state=algoithm_parameters_dict["random_state"],
                           solver=algoithm_parameters_dict["solver"],
                           max_iter=algoithm_parameters_dict["max_iter"],
                           multi_class=algoithm_parameters_dict["multi_class"],
                           verbose=algoithm_parameters_dict["verbose"],
                           warm_start=algoithm_parameters_dict["warm_start"],
                           n_jobs=algoithm_parameters_dict["n_jobs"])

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

