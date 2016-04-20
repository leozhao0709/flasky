# -*- coding: utf-8 -*-

__author__ = 'lzhao'
__date__ = '3/27/16'
__time__ = '1:08 PM'

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASK_MAIL_SUBJECT_PREFIX = '[Flask]'
	FLASK_MAIL_SENDER = 'Flask Admin <flask@example.com>'
	FLASK_ADMIN = os.environ.get('FLASK_MAIL_USERNAME')
	FLASKY_POSTS_PER_PAGE = 20
	FLASKY_FOLLOWERS_PER_PAGE = 50
	FLASKY_COMMENTS_PER_PAGE = 30
	FLASKY_SLOW_DB_QUERY_TIME = 0.5

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('FLASK_MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('FLASK_MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or "mysql://{user}:{password}@{host}/flasky".format(
		user=os.environ.get("DB_USER"),
		password=os.environ.get("DB_PASS"), host=os.environ.get("DB_HOST"))


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get(
		'DEV_DATABASE_URL') or "mysql://{user}:{password}@{host}/flaskyTest".format(
		user=os.environ.get("DB_USER"),
		password=os.environ.get("DB_PASS"), host=os.environ.get("DB_HOST"))


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get(
		'DEV_DATABASE_URL') or "mysql://{user}:{password}@{host}/flasky".format(
		user=os.environ.get("DB_USER"),
		password=os.environ.get("DB_PASS"), host=os.environ.get("DB_HOST"))


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}
