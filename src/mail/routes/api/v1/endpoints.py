import os
from flask import Blueprint, request, jsonify
from src.mail.controllers import send, check
from src.helpers.generic_errors.main import error

endpoints_routes = Blueprint('endpoints_routes', __name__,)

@endpoints_routes.route('/mail/send', strict_slashes=False, methods=['POST'])
def send_mail_endpoint():
    if request.data:
        return error(status=400, error_message="Empty payload")
    return send.send_mail(request.data)

@endpoints_routes.route('/mail/check', strict_slashes=False, methods=['GET'])
def check_mail_endpoint():
    return check.check_mail()
