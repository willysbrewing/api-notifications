import os
from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from src.mail.controllers import send
from src.mail.serializers import sendmail
from src.helpers.generic_errors.main import error

endpoints_routes = Blueprint('endpoints_routes', __name__,)

@endpoints_routes.route('/mail/send', strict_slashes=False, methods=['POST'])
@cross_origin()
def send_mail_endpoint():
    if not request.get_json():
        return error(status=400, error_message="Empty payload")

    response = send.execute(request.get_json())
    if 'error_message' in response:
        return error(status=response['status'], error_message=response['error_message'])

    data = sendmail.serialize(message=response['message'])
    return jsonify(data), 200
