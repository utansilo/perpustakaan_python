from flask import jsonify

def success_message(data=None, message="Success", status_code=200):
    response = {
        "success" : True,
        "message" : message
    }

    if data is not None:
        response['data'] = data

    return jsonify(response), status_code

def error_message(message="Error", status_code=400):
    return jsonify({
        "success" : False,
        "message" : message
    }), status_code