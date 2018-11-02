from flask import request, abort, Flask, jsonify, make_response, Response
from data import ModelProcessor as mp
from config import ConfigManager
from DatasetConnector import DatasetConnectorFactory as dcf
from CustomException import CustomException as CE
from handler import PredictService as PR, TrainService as TR , ModelService as GMS
from threading import Thread
import logging.config
from logs import LogHandler
from handler import LoadModelService as LMS

ErrorLogger = logging.getLogger("ErrorLogs")
InfoLogger = logging.getLogger("InfoLogs")
LogHandler.setup_logging()

app = Flask(__name__)


@app.route('/todo/api/v1.0/PredictionAnalytics/CheckDatasetConnection', methods=['POST'])
def check_dataset_connection():

    if not request.json:
        abort(ConfigManager.error_code_400)

    json_data = request.json
    response_json = dict()
    response_code = 200

    try:
            response_json["success"] = dcf.DatasetConnectorFactory().check_connection(json_data["dbconnect"])

    except Exception as e:
        ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up', 500)
        response_json["success"] = False
        response_json["message"] = "EXCEPTION 500: Damm! Something Blew up"
        response_code = 500

    return jsonify(response_json), response_code


@app.route('/todo/api/v1.0/PredictionAnalytics/GetDatasetColumnList', methods=['POST'])
def GetDatasetColumnList():

    if not request.json:
        abort(ConfigManager.error_code_400)

    json_data = request.json
    response_json = dict()
    response_json["success"] = True
    response_code = 200

    try:

        if not dcf.DatasetConnectorFactory().check_connection(json_data["dbconnect"]):
            raise CE.DatasetConnectionFailed("Failed to establish connection with dataset connector: %s"
                                             % (json_data["dbconnect"]["name"]), 403)

        column_list = dcf.DatasetConnectorFactory().get_column_list(json_data["dbconnect"])

        if column_list:
            response_json["columnList"] = column_list
        else:
            response_json["success"] = False

    except CE.DatasetConnectionFailed as e:
        ErrorLogger.exception('EXCEPTION %s: Bad Dataset connection Params "%s"', str(e.errors), str(e))
        response_json["success"] = False
        response_json["message"] = str(e)
        response_code = int(e.errors)

    except Exception as e:
        ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up', 500)
        response_json["success"] = False
        response_json["message"] = "EXCEPTION 500: Damm! Something Blew up"
        response_code = 500

    return jsonify(response_json), response_code


@app.route('/todo/api/v1.0/PredictionAnalytics/TrainModel', methods=['POST'])
def train_model():

    if not request.json:
        abort(ConfigManager.error_code_400)

    json_data = request.json
    response_json = dict()
    response_json["success"] = True
    response_json["message"] = "InProgress"
    response_code = 200

    try:
        if ConfigManager.algo_list.get(json_data["algorithm"]["name"]) is None:
            raise CE.BadAlgorithmParams("Algorithm does not exist", 402)

        elif mp.ModelProcessor().get_model_mongo_byAppIdandmodelName_count(json_data) > 0:
            raise CE.BadAlgorithmParams("Model name already exist for this app id", 403)

        elif not dcf.DatasetConnectorFactory().check_connection(json_data["dbconnect"]):
            raise CE.DatasetConnectionFailed("Failed to establish connection with dataset connector: %s"
                                             % (json_data["dbconnect"]["name"]), 403)

        thread = Thread(target=TR.TrainService().train_model, args=(json_data,))
        thread.start()
        InfoLogger.info("Step1: New thread started to do model training for Appid: %s and Modelname: %s",
                        str(json_data["appId"]), str(json_data["modelName"]))

    except CE.BadAlgorithmParams as e:
        ErrorLogger.exception('EXCEPTION %s: Bad Algorithm Params "%s"', str(e.errors), str(e))
        response_json["success"] = False
        response_json["message"] = str(e)
        response_code = int(e.errors)

    except CE.DatasetConnectionFailed as e:
        ErrorLogger.exception('EXCEPTION %s: Bad Dataset connection Params "%s"', str(e.errors), str(e))
        response_json["success"] = False
        response_json["message"] = str(e)
        response_code = int(e.errors)

    except Exception as e:
        ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up', 500)
        response_json["success"] = False
        response_json["message"] = "EXCEPTION 500: Damm! Something Blew up"
        response_code = 500

    return jsonify(response_json), response_code


@app.route('/todo/api/v1.0/PredictionAnalytics/GetAllModel', methods=['POST'])
def get_all_model():

    if not request.json:
        abort(ConfigManager.error_code_400)

    json_data = request.json
    response_json = dict()
    response_json["success"] = True
    response_code = 200

    try:
        if mp.ModelProcessor().get_model_mongo_byAppId_count(json_data) == 0:
            raise CE.ModelDoesNotExist("No model(s) exist", 403)

        response_json["allModelValues"] = GMS.ModelService().get_all_model_details(json_data)

    except CE.ModelDoesNotExist as e:
        ErrorLogger.exception('EXCEPTION %s: NO such model "%s"', str(e.errors), str(e))
        response_json["success"] = False
        response_json["message"] = str(e)
        response_code = int(e.errors)

    except Exception as e:
        ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up', 500)
        response_json["success"] = False
        response_json["message"] = "EXCEPTION 500: Damm! Something Blew up"
        response_code = 500

    return jsonify(response_json), response_code


@app.route('/todo/api/v1.0/PredictionAnalytics/GetModel', methods=['POST'])
def get_model():

    if not request.json:
        abort(ConfigManager.error_code_400)

    json_data = request.json
    response_json = dict()
    response_json["success"] = True
    response_code = 200

    try:
        if mp.ModelProcessor().get_model_mongo_byAppIdandmodelName_count(json_data) == 0:
            raise CE.ModelDoesNotExist("No model(s) exist", 403)

        response_json["allModelValues"] = GMS.ModelService().get_model_details(json_data)
        print (response_json)

    except CE.ModelDoesNotExist as e:
        ErrorLogger.exception('EXCEPTION %s: NO such model "%s"', str(e.errors), str(e))
        response_json["success"] = False
        response_json["message"] = str(e)
        response_code = int(e.errors)

    except Exception as e:
        ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up', 500)
        response_json["success"] = False
        response_json["message"] = "EXCEPTION 500: Damm! Something Blew up"
        response_code = 500

    return jsonify(response_json), response_code


@app.route('/todo/api/v1.0/PredictionAnalytics/DeleteModel', methods=['DELETE'])
def delete_model():

    if not request.json:
        abort(ConfigManager.error_code_400)

    json_data = request.json
    response_json = dict()
    response_json["success"] = True
    response_code = 200

    try:
        if mp.ModelProcessor().get_model_mongo_byAppIdandmodelName_count(json_data) == 0:
            raise CE.ModelDoesNotExist("Model name does not exist", 403)

        GMS.ModelService().delete_model(json_data)

    except CE.ModelDoesNotExist as e:
        ErrorLogger.exception('EXCEPTION %s: NO such model "%s"', str(e.errors), str(e))
        response_json["success"] = False
        response_json["message"] = str(e)
        response_code = int(e.errors)

    except Exception as e:
        ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up', 500)
        response_json["success"] = False
        response_json["message"] = "EXCEPTION 500: Damm! Something Blew up"
        response_code = 500

    return jsonify(response_json), response_code


@app.route('/todo/api/v1.0/PredictionAnalytics/DeployModel', methods=['POST'])
def load_model():
    if not request.json:
        abort(ConfigManager.error_code_400)

    json_data = request.json
    response_json = dict()
    response_json["success"] = True
    response_json["message"] = "InProgress"
    response_code = 200

    try:
        if mp.ModelProcessor().get_model_mongo_byAppIdandmodelName_count(json_data) == 0:
            raise CE.ModelDoesNotExist("Model name does not exist", 403)

        elif LMS.LoadModelService().check_if_model_load(json_data):
            raise CE.ModelAlreadyInMemory("Model already deployed", 403)

        thread = Thread(target=LMS.LoadModelService().load_model, args=(json_data,))
        thread.start()

        InfoLogger.info("New thread started to load model for Appid: %s and Modelname: %s",
                        str(json_data["appId"]), str(json_data["modelName"]))

    except CE.ModelDoesNotExist as e:
        ErrorLogger.exception('EXCEPTION %s: NO such model "%s"', str(e.errors), str(e))
        response_json["success"] = False
        response_json["message"] = str(e)
        response_code = int(e.errors)

    except CE.ModelAlreadyInMemory as e:
        ErrorLogger.exception('EXCEPTION %s: NO such model "%s"', str(e.errors), str(e))
        response_json["success"] = False
        response_json["message"] = str(e)
        response_code = int(e.errors)

    except Exception as e:
        ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up', 500)
        response_json["success"] = False
        response_json["message"] = "EXCEPTION 500: Damm! Something Blew up"
        response_code = 500

    return jsonify(response_json), response_code


@app.route('/todo/api/v1.0/PredictionAnalytics/UnLoadModel', methods=['POST'])
def unload_model():
    if not request.json:
        abort(ConfigManager.error_code_400)

    json_data = request.json
    response_json = dict()
    status = dict()
    response_code = 200

    try:
        if not LMS.LoadModelService().check_if_model_load(json_data):
            raise CE.ModelNotInMemory("No such model loaded", 403)

        response_json["success"] = LMS.LoadModelService().unload_model(json_data)
        status["loaded"] = False
        mp.ModelProcessor().update_key_mongo(json_data["appId"], json_data["modelName"], status)

    except CE.ModelNotInMemory as e:
        ErrorLogger.exception('EXCEPTION %s: NO such model "%s"', str(e.errors), str(e))
        response_json["success"] = False
        response_json["message"] = str(e)
        response_code = int(e.errors)

    except Exception as e:
        ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up', 500)
        response_json["success"] = False
        response_json["message"] = "EXCEPTION 500: Damm! Something Blew up"
        response_code = 500

    return jsonify(response_json), response_code


@app.route('/todo/api/v1.0/PredictionAnalytics/Predict', methods=['POST'])
def predict():

    if not request.json:
        abort(ConfigManager.error_code_400)

    json_data = request.json
    response_json = dict()
    response_json["success"] = True
    response_code = 200

    try:
        if mp.ModelProcessor().get_model_mongo_byAppIdandmodelName_count(json_data) == 0:
            raise CE.ModelDoesNotExist("Model name does not exist", 403)

        elif not LMS.LoadModelService().check_if_model_load(json_data):
            raise CE.ModelNotInMemory("Model not deployed, Please deploy model", 403)

        response_json["prediction"] = str(PR.PredictService().predict_service(json_data))

    except CE.ModelDoesNotExist as e:
        ErrorLogger.exception('EXCEPTION %s: NO such model "%s"', str(e.errors), str(e))
        response_json["success"] = False
        response_json["message"] = str(e)
        response_code = int(e.errors)

    except CE.ModelNotInMemory as e:
        ErrorLogger.exception('EXCEPTION %s: NO such model "%s"', str(e.errors), str(e))
        response_json["success"] = False
        response_json["message"] = str(e)
        response_code = int(e.errors)

    except CE.InvalidPredictionParams as e:
        ErrorLogger.exception('EXCEPTION %s:Invalid Prediction Params "%s"', str(e.errors), str(e))
        response_json["success"] = False
        response_json["message"] = str(e)
        response_code = int(e.errors)

    except Exception as e:
        ErrorLogger.exception('EXCEPTION %s: Damm! Something Blew up', 500)
        response_json["success"] = False
        response_json["message"] = "EXCEPTION 500: Damm! Something Blew up"
        response_code = 500

    return jsonify(response_json), response_code


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Invalid Request'}), 400)


@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'success': 'False', 'message': 'EXCEPTION 500: Damm! Something Blew up'}), 500)


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0',port=int("6060"), threaded=True)

