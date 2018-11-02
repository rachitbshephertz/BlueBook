import pickle
import os , json
import ast
from config import ConfigManager
from keras.models import Sequential
from keras.layers import Dense


class NeuralNetwork(object):

    def __init__(self):
        pass

    def train(self,split_params, model_dict):
        algo_parameters_dict = ConfigManager.random_forest_classifier_list
        Directory = ConfigManager.ROOT_DIR + "/TrainedModelsDirectory"
        filename = str(model_dict["modelName"]) + "_" + str(model_dict["algorithm"]["name"]) + "_" \
                   + str(model_dict["appId"]) + ".sav"
        filepath = os.path.join(Directory, filename)
        isDefault = str(model_dict["algorithm"]["isDefault"])

        if 'False' in isDefault:
            pass

        print(model_dict)
        # create model
        trained_model = Sequential()
        # Input Layer
        trained_model.add(Dense(12, input_dim=len(split_params["features_train"].columns), activation=model_dict["algorithm"]["parameters"]["activationInputLayer"]))
        # Hidden Layer
        for hiddenLayer in model_dict["algorithm"]["parameters"]["hiddenLayers"]:
            hiddenLayer = ast.literal_eval(hiddenLayer)
            if (hiddenLayer["type"]) == "Dense":
                trained_model.add(Dense(hiddenLayer["neurons"], activation=hiddenLayer["activation"]))

        # Output Layer
        trained_model.add(Dense(len(split_params["target_train"].columns), activation=model_dict["algorithm"]["parameters"]["activationOutputLayer"]))

        # Compile model
        trained_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Fit the model
        trained_model.fit(split_params["features_train"], split_params["target_train"], epochs=150, batch_size=10)

        # save the model to disk
        files = open(filepath, 'wb')
        pickle.dump(trained_model, files, protocol=pickle.HIGHEST_PROTOCOL)
        files.close()

        # evaluate the model
        accuracy = trained_model.evaluate(split_params["features_test"], split_params["target_test"])
        accuracy = accuracy[1]*100
        model_dict["accuracy"] = accuracy
        return model_dict
