# -*- coding: utf-8 -*-

__author__ = 'lzhao'
__date__ = '3/27/16'
__time__ = '1:06 PM'

from . import mail
from flask.ext.mail import Message
from threading import Thread
from flask import render_template, current_app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASK_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
