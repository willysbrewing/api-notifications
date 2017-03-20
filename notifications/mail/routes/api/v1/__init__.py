from flask import Blueprint

endpoints = Blueprint('endpoints', __name__)
import mail_router
