# -*- coding: utf-8 -*-

__author__ = 'lzhao'
__date__ = '4/10/16'
__time__ = '9:00 PM'

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, DataRequired


class LoginForm(Form):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('keep me logged in')
	submit = SubmitField('Log In')
