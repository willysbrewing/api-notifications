import json
import sendgrid
from sendgrid.helpers.mail import *

f = open("config/secrets.json", 'r')
secrets = json.loads(f.read())
f.close()

SENDGRID_API_KEY = secrets['SENDGRID_API_KEY']
SENDGRID_API_SENDER = secrets['SENDGRID_API_SENDER']

# Wrapper
def execute(payload):
    try:
        recipient = payload['recipient']
        subject = payload['subject']
        content = payload['content']
        template = None
        list_id = 717988 # ListID @TODO generic

        if not content:
            content = 'notset'
        if not subject:
            subject = 'notset'
        if 'template' in payload:
            template = payload['template'] # template.id & template.data
        if 'list_id' in payload:
            list_id = payload['list_id']
    except Exception as e:
        return {'status':400, 'error_message':"Wrong payload: "+str(e)}

    return SendMail(recipient, subject, content, template, list_id).execute() # send

class SendMail:
    def __init__(self, recipient, subject, content, template, list_id):
        self.recipient = recipient
        self.subject = subject
        self.content = Content('text/html', content)
        self.template = template
        self.sender = SENDGRID_API_SENDER
        self.list_id = list_id
        self.sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)


    def execute(self):
        mail = Mail(Email(self.sender), self.subject, Email(self.recipient), self.content)

        if self.template:
            self.set_template(mail)

        response = self.sg.client.mail.send.post(request_body=mail.get())

        if (response.status_code != 200) and (response.status_code != 202):
            return {'status':response.status_code, 'error_message':response.body}

        if self.list_id:
            return self.store_contact()
        else:
            return {'message': 'Email Sent'}

    def set_template(self, mail):
        if self.template['id'] == "c348a464-4240-4cf4-9c88-7b2c892070d7":
            name = self.template['data']['name'].encode('utf-8')
            mail.personalizations[0].add_substitution(Substitution("-name-", name))
            mail.set_template_id(self.template['id'])

    def store_contact(self):
        contact_data = [
            {
                "email": self.recipient,
                "first_name": "" #@TODO last name?
            }
        ]

        if self.template != None and 'name' in self.template['data']:
            contact_data[0]['first_name'] = self.template['data']['name']

        # Create contact
        response = self.sg.client.contactdb.recipients.post(request_body=contact_data)
        if (response.status_code != 200) and (response.status_code != 201):
            return {'status':response.status_code, 'error_message':response.body}

        # Get ContactId
        recipient_id = json.loads(response.body)['persisted_recipients'][0]

        # Store in List
        response = self.sg.client.contactdb.lists._(self.list_id).recipients._(recipient_id).post()
        if (response.status_code != 200) and (response.status_code != 201):
            return {'status':response.status_code, 'error_message':response.body}

        return {'message': 'Email Sent and Contact Saved'}
