import json
import sendgrid
from sendgrid.helpers import mail
from src.helpers.generic_errors.main import error
from flask import Flask, jsonify

f = open("config/secrets.json", 'r')
secrets = json.loads(f.read())
f.close()

SENDGRID_API_KEY = secrets['SENDGRID_API_KEY']
SENDGRID_API_SENDER = secrets['SENDGRID_API_SENDER']

# @TODO: Class!

def send_mail(payload):
    try:
        to_email = payload['recipient']
        subject = payload['subject']
        content = payload['content']
    except Exception as e:
        return error(status=400, error_message="Wrong payload")
    return execute(to_email, subject, content)

def execute(to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

    from_email = mail.Email(SENDGRID_API_SENDER)
    content = mail.Content('text/plain', content)
    to_email = mail.Email(to_email)
    message = mail.Mail(from_email, subject, to_email, content)

    response = sg.client.mail.send.post(request_body=message.get())

    if (response.status_code != 200) and (response.status_code != 202):
        return error(status=response.status_code, error_message=response.body)

    return jsonify({'message': 'Email Sent'}), 200
