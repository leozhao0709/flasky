# -*- coding: utf-8 -*-

__author__ = 'lzhao'
__date__ = '4/10/16'
__time__ = '9:00 PM'

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Email, DataRequired, Length, Regexp, EqualTo
from wtforms.fields.html5 import EmailField
from app.models import User


class LoginForm(Form):
	email = EmailField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(4, 64)])
	remember_me = BooleanField('keep me logged in')
	submit = SubmitField('Log In')


class RegistrationForm(Form):
	email = EmailField('Email', validators=[DataRequired(), Email()])

	username = StringField('Username', validators=[DataRequired(), Length(3, 64), Regexp('^[A-Za-z][\w\d_.]*$', 0,
																						 'username must start with letter and can only contain letter, number, dot or under_score')])
	password = PasswordField('Password', validators=[DataRequired(), Length(4, 64)])
	password2 = PasswordField('Password2', validators=[DataRequired(), Length(4, 64),
													   EqualTo('password', message='Password must match')])
	submit = SubmitField('Register')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')


class PasswordResetRequestForm(Form):
	email = EmailField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
	password = PasswordField('New Password', validators=[DataRequired()])
	password2 = PasswordField('Confirm password',
							  validators=[DataRequired(), EqualTo('password', message='Password must match')])
	submit = SubmitField('Reset Password')
