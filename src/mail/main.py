# [START app]
import logging

from flask import Flask
from routes.api.v1.endpoints import endpoints_routes

app = Flask(__name__) # Flask app
app.register_blueprint(endpoints_routes) # Matching routing (api/v1)
