from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def email_message_send(subject, message,receiver):
    email = EmailMessage(
        subject,
        message,
        'Blue Revelle Inc <headoffice@bluerevelleinc.com>',
        [receiver],
        )
    email.content_subtype = "html"
    email.fail_silently = False
    email.send()
    return message
