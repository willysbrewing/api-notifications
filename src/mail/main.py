import logging

from flask import Flask
from src.helpers.generic_errors.main import app
from routes.api.v1.endpoints import endpoints_routes

# generic app from error_main
app.register_blueprint(endpoints_routes) # Matching routing (api/v1)
