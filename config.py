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
	SQLALCHEMY_RECORD_QUERIES = True
	SSL_DISABLE = True

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

	@classmethod
	def init_app(cls, app):
		Config.init_app(app)

		# email errors to the administrators
		import logging
		from logging.handlers import SMTPHandler
		credentials = None
		secure = None
		if getattr(cls, 'MAIL_USERNAME', None) is not None:
			credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
			if getattr(cls, 'MAIL_USE_TLS', None):
				secure = ()
		mail_handler = SMTPHandler(
			mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
			fromaddr=cls.FLASKY_MAIL_SENDER,
			toaddrs=[cls.FLASKY_ADMIN],
			subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
			credentials=credentials,
			secure=secure)
		mail_handler.setLevel(logging.ERROR)
		app.logger.addHandler(mail_handler)


class UnixConfig(ProductionConfig):
	@classmethod
	def init_app(cls, app):
		ProductionConfig.init_app(app)

		# log to syslog
		# With this configuration, application logs will be written to /var/log/messages(from book) or /var/run/syslog(from code).
		import logging
		from logging.handlers import SysLogHandler
		syslog_handler = SysLogHandler()
		syslog_handler.setLevel(logging.WARNING)
		app.logger.addHandler(syslog_handler)


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}
