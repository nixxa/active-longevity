# -*- coding: utf-8 -*-
"""
Manage module
"""
#pylint: disable=C0103
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from application import app, db #pylint: disable=E0401
from management import ImportCommand #pylint: disable=E0401

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('import', ImportCommand())

if __name__ == '__main__':
    manager.run()
