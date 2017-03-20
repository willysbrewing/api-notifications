from notifications.mail.models import SendMail, SendMailSchema

def serialize(message):
    sendmail = SendMail(message=message)
    response = SendMailSchema().dump(sendmail)
    return response.data
