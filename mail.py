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
    to = 'ogbonnajay@gmail.com'
    send_email('ogbonnajay@gmail.com', 'Another test mail for configuration')
    return 'Mail sent to ogbonnajay@gmail Successfuly!'