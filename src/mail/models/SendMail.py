from marshmallow import Schema, fields

class SendMail:
    def __init__(self, message):
        self.message = message

class SendMailSchema(Schema):
      message = fields.Str()
