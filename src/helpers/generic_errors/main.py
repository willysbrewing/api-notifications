import logging

from flask import Flask, jsonify
import errorserializer

app = Flask(__name__)

def error(status, error_message):
    data = errorserializer.serialize(status, error_message=error_message)
    logging.error(error_message)
    return jsonify(data), status

@app.errorhandler(500)
def server_error(e):
    return error(status=500, error_message='An internal error occurred')

@app.errorhandler(400)
def bad_request(e):
    return error(status=400, error_message='Bad request')

@app.errorhandler(404)
def not_found(e):
    return error(status=404, error_message='Not found')

@app.errorhandler(405)
def not_allowed(e):
    return error(status=405, error_message='Method not allowed')
