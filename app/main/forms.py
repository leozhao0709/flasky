# -*- coding: utf-8 -*-
from app.models import Role, User
from wtforms.fields.html5 import EmailField

__author__ = 'lzhao'
__date__ = '4/8/16'
__time__ = '9:10 PM'

from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError
from flask_pagedown.fields import PageDownField


class EditProfileForm(Form):
	name = StringField('Real name', validators=[Length(0, 64)])
	location = StringField('Location', validators=[Length(0, 64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
	email = EmailField('Email', validators=[DataRequired(), Email()])
	username = StringField('Username', validators=[DataRequired(), Length(3, 64), Regexp('^[A-Za-z][\w\d_.]*$', 0,
																						 'username must start with letter and can only contain letter, number, dot or under_score')])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role', coerce=int)
	name = StringField('Real name', validators=[Length(0, 64)])
	location = StringField('Location', validators=[Length(0, 64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')

	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self, field):
		if field.data != self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if field.data != self.user.username and User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use')


class PostForm(Form):
	body = PageDownField("What's on your mind?", validators=[DataRequired()])
	submit = SubmitField('Submit')


class CommentForm(Form):
	body = PageDownField('Enter your comment', validators=[DataRequired()])
	submit = SubmitField('Submit')
