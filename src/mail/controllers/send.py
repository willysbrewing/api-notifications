import json
import sendgrid
from sendgrid.helpers import mail
from src.helpers.generic_errors.main import error

f = open("config/secrets.json", 'r')
secrets = json.loads(f.read())
f.close()

SENDGRID_API_KEY = secrets['SENDGRID_API_KEY']
SENDGRID_SENDER = secrets['SENDGRID_API_SENDER']

def send_mail(payload):
    try:
        to_email = payload.recipient
        subject = payload.subject
        content = payload.content
    except Exception as e:
        return error(status=400, error_message="Wrong payload")
    execute()

def execute(to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

    from_email = mail.Email(SENDGRID_SENDER)
    content = mail.Content('text/plain', content)
    message = mail.Mail(from_email, subject, to_email, content)

    response = sg.client.mail.send.post(request_body=message.get())
    return response
