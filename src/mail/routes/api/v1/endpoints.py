import os
from flask import request, jsonify, Blueprint

endpoints_routes = Blueprint('endpoints_routes', __name__,)

@endpoints_routes.route('/mail/send', strict_slashes=False)
def send_mail():
    return 'Send Mail'

@endpoints_routes.route('/mail/check', strict_slashes=False)
def check_mail():
    return 'Check Mail'
