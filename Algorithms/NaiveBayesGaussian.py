import pickle
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from config import ConfigManager
import os
import ast

class NaiveBayesGaussian(object):

    def __init__(self):
        pass


    def train(self,split_params, model_dict):
        algoithm_parameters_dict = ConfigManager.naive_bayes_gaussianNB_list

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

        trained_model = GaussianNB(priors=algoithm_parameters_dict["priors"])

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

