from flask import request, abort, Flask, jsonify, make_response
from config import ConfigManager


app = Flask(__name__)


@app.route('/todo/api/v1.0/Put', methods=['PUT'])
def get_all_model():
    response_json = dict()

    print "Headers"
    print request.headers
    print "BODY"
    print request.json
    print
    print request.query_string

    response_json["BODY"] = request.json
    response_json["QUERY"] = request.query_string

    return jsonify(response_json), 200


@app.route('/todo/api/v1.0/Post', methods=['POST'])
def get_model():
    if not request.json:
        abort(ConfigManager.error_code_400)

    response_json = dict()

    print "Headers"
    print request.headers
    print "BODY"
    print request.json
    print "QUERY"
    print request.query_string

    response_json["BODY"] = request.json
    response_json["QUERY"] = request.query_string

    return jsonify(response_json), 200


@app.route('/todo/api/v1.0/Delete', methods=['DELETE'])
def delete_model():
    if not request.json:
        abort(ConfigManager.error_code_400)

    response_json = dict()

    print "Headers"
    print request.headers
    print "BODY"
    print request.json
    print "QUERY"
    print request.query_string


    response_json["BODY"] = request.json
    response_json["QUERY"] = request.query_string

    return jsonify(response_json), 200


@app.route('/todo/api/v1.0/Get', methods=['GET'])
def load_model():
    response_json = dict()

    print "Headers"
    print request.headers
    print "QUERY"
    print request.query_string

    response_json["QUERY"] = request.query_string

    return jsonify(response_json), 200



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

