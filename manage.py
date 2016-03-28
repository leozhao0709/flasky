# -*- coding: utf-8 -*-

import os
from app import create_app, db
# from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

__author__ = 'lzhao'
__date__ = '3/27/16'
__time__ = '1:07 PM'

app = create_app(os.getenv('FLASK_CONFIG'))
manager = Manager(app)
Migrate = Migrate(app, db)


def make_shell_context():
	return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
