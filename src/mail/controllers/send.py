import json
import sendgrid
from sendgrid.helpers.mail import *
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
        template = None
        if 'template' in payload:
            template = payload['template'] # template.id & template.data
    except Exception as e:
        return error(status=400, error_message="Wrong payload")
    return execute(to_email, subject=subject, content=content,
                   template=template)

def execute(to_email, subject=None, content=None, template=None):
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

    from_email = Email(SENDGRID_API_SENDER)
    to_email = Email(to_email)

    if not content:
        content = 'notset'
    if not subject:
        subject = 'notset'

    content = Content('text/html', content)
    mail = Mail(from_email, subject, to_email, content)

    if template:
        set_template(mail, template['id'], template['data'])

    response = sg.client.mail.send.post(request_body=mail.get())

    if (response.status_code != 200) and (response.status_code != 202):
        return error(status=response.status_code, error_message=response.body)

    return jsonify({'message': 'Email Sent'}), 200

def set_template(mail, id, data):
    if id == "c348a464-4240-4cf4-9c88-7b2c892070d7":
        mail.personalizations[0].add_substitution(Substitution("-name-", data['name']))
        mail.set_template_id(id)
