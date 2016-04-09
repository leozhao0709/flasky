# -*- coding: utf-8 -*-

__author__ = 'lzhao'
__date__ = '4/8/16'
__time__ = '9:10 PM'

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(Form):
	name = StringField('What is your name?', validators=[DataRequired()])
	submit = SubmitField('Submit')
