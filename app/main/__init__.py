# -*- coding: utf-8 -*-
from app.models import Permission
from flask import Blueprint

__author__ = 'lzhao'
__date__ = '3/27/16'
__time__ = '1:05 PM'

main = Blueprint('main', __name__)

from . import views, errors


@main.app_context_processor
def inject_permissions():
	return dict(Permission=Permission)
