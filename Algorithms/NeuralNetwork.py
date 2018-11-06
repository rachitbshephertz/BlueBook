import pickle
import os , json
import ast
from config import ConfigManager
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf
import keras
from keras import backend as K

class NeuralNetwork(object):

    def __init__(self):
        pass

    def train(self,split_params, model_dict):
        Directory = ConfigManager.ROOT_DIR + "/TrainedModelsDirectory"
        filename = str(model_dict["modelName"]) + "_" + str(model_dict["algorithm"]["name"]) + "_" \
                   + str(model_dict["appId"]) + ".hdf5"
        sessName = str(model_dict["modelName"]) + "_" + str(model_dict["algorithm"]["name"]) + "_" \
                   + str(model_dict["appId"])
        sessPath = os.path.join(Directory, sessName)
        filepath = os.path.join(Directory, filename)
        isDefault = str(model_dict["algorithm"]["isDefault"])

        if 'False' in isDefault:
            pass
        K.clear_session()

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
        trained_model.compile(loss=model_dict["algorithm"]["parameters"]["loss"],
                              optimizer=model_dict["algorithm"]["parameters"]["optimizer"],
                              metrics=model_dict["algorithm"]["parameters"]["metrics"])

        # Fit the model
        trained_model.fit(split_params["features_train"], split_params["target_train"],
                          epochs=model_dict["algorithm"]["parameters"]["epochs"], batch_size=model_dict["algorithm"]["parameters"]["batchSize"])

        # Save trained model and session
        saver = tf.train.Saver()
        sess = keras.backend.get_session()
        saver.save(sess, sessPath)
        trained_model.save(filepath)

        # evaluate the model
        accuracy = trained_model.evaluate(split_params["features_test"], split_params["target_test"])
        accuracy = round(accuracy[1]*100,2)
        model_dict["accuracy"] = accuracy
        return model_dict
