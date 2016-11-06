from marshmallow import Schema, fields

class Error:
    def __init__(self, status, detail):
        self.status = status
        self.detail = detail

class ErrorSchema(Schema):
      status = fields.Integer()
      detail = fields.Str()
