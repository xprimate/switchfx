from flask import (
    Blueprint, Flask, g, redirect, render_template, request, url_for, session, flash, current_app
)
from flask_mail import Message
from flask_mail import Mail
from switchfx import mail_obj


bp = Blueprint('mail', __name__)
def send_email(to, subject):
    msg = Message(
        subject,
        recipients=[to],
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail_obj.send(msg)


@bp.route('/mail')
def index():
    subject = 'This is a test mail'
    to = 'ogbonnerrerajay@gmail.com'
    send_email('ogbeeronnajay@gmail.com', 'Another test mail for configuration')
    return 'Mail sent to ogboerernnajay@gmail Successfuly!'


def mail_thread_owner(thread_owner_user_name, thread_owner_email, message):
    subject = "Forex update for  %s " % thread_owner_user_name + "  "
    msg = Message(recipients=[thread_owner_email],
                        body=message,
                        subject=subject)
    mail_obj.send(msg)
    
 
def send_mails(users, message):
   
    with mail_obj.connect() as conn:
        for user in users:
           # message = 'Follow the link to view'
            subject = "Hello %s " % user['user_name'] + ", their is comment update" 
            msg = Message(recipients=[user['email']],
                        body=message,
                        subject=subject)

            conn.send(msg)

def reset_mail(users, recover_url):
    with mail_obj.connect() as conn:
        for user in users:

            message = "Hello %s " % user['first_name'] + ", please click on the link to reset your password.\r\n"+ recover_url
            subject = "Password Reset for  %s " % user['first_name'] + "  "
            msg = Message(recipients=[user['email']],
                        body=message,
                        subject=subject)

            conn.send(msg)