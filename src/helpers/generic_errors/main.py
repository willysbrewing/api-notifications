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
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return jsonify({'message': 'An internal error occurred.'}), 500

@app.errorhandler(400)
def bad_request(e):
    logging.exception('Bad request')
    return jsonify({'message': 'Bad request'}), 400

@app.errorhandler(404)
def not_found(e):
    logging.exception('Not found')
    return jsonify({'message': 'Not Found'}), 404

@app.errorhandler(405)
def not_allowed(e):
    logging.exception('Method not allowed')
    return jsonify({'message': 'Method not allowed'}), 405
