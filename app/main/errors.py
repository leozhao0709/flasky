# -*- coding: utf-8 -*-

__author__ = 'lzhao'
__date__ = '3/27/16'
__time__ = '1:06 PM'

from flask import render_template, request
from . import main


@main.app_errorhandler(403)
def forbidden(e):
	return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500
