# main/mail/functions.py

from flask import current_app, render_template
from flask_mail import Message
from smtplib import SMTPException
from .. import mailsender  # Importar mailsender

def sendMail(to, subject, template, **kwargs):
    # Configuración del mail
    msg = Message(subject, sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=to)
    try:
        # Creación del cuerpo del mensaje
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        # Envío de mail
        mailsender.send(msg)  # Usar mailsender para enviar el mensaje
    except SMTPException as e:
        print(str(e))
        return "Mail deliver failed"
    return True
