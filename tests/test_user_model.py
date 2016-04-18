# -*- coding: utf-8 -*-

from test_basics import BasicsTestCase
from app.models import User, Role, Permission, AnonymousUser

__author__ = 'lzhao'
__date__ = '4/10/16'
__time__ = '3:25 PM'


class UserModelTestCase(BasicsTestCase):
	def test_password_setter(self):
		u = User(password='cat')
		self.assertTrue(u.password_hash is not None)

	def test_no_password_getter(self):
		u = User(password='cat')
		with self.assertRaises(AttributeError):
			u.password

	def test_password_verification(self):
		u = User(password='cat')
		self.assertTrue(u.verify_password('cat'))
		self.assertFalse(u.verify_password('dog'))

	def test_password_salts_are_random(self):
		u = User(password='cat')
		u2 = User(password='cat')
		self.assertTrue(u.password_hash != u2.password_hash)

	def test_roles_and_permissions(self):
		Role.insert_roles()
		u = User(email='zha434@usc.edu', password='')
		self.assertTrue(u.can(Permission.WRITE_ARTICLES))
		self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

	def test_anonymous_user(self):
		u = AnonymousUser()
		self.assertFalse(u.can(Permission.FOLLOW))
