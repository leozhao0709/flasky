# -*- coding: utf-8 -*-

import os
from app import create_app, db
from app.models import User, Role, Post, Follow
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

__author__ = 'lzhao'
__date__ = '3/27/16'
__time__ = '1:07 PM'

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
Migrate = Migrate(app, db)


def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role, Post=Post, Follow=Follow)


@manager.command
def test():
	"""run the unit tests."""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
	"""run deployment tasks."""
	from flask_migrate import upgrade

	# migrate database to latest revision
	upgrade()

	# create user roles
	Role.insert_roles()

	# create self-follows for all users
	User.add_self_follows()

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
