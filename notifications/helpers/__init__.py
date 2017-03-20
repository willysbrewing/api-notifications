import logging

from flask import Flask, jsonify
from marshmallow import Schema, fields

class Error:
    def __init__(self, status, detail):
        self.status = status
        self.detail = detail


class ErrorSchema(Schema):
    status = fields.Integer()
    detail = fields.Str()


def serialize(status, error_message):
    error = Error(status=status, detail=error_message)
    errors = [error] # make it iterable so response can contain a list of errs
    response = ErrorSchema(many=True).dump(errors)
    return {'errors': response.data} # particular dict response (in this case)


def error(status, error_message):
    data = serialize(status, error_message=error_message)
    logging.error(error_message)
    return jsonify(data), status
