# -*- coding: utf-8 -*-

__author__ = 'lzhao'
__date__ = '4/10/16'
__time__ = '6:32 PM'

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
