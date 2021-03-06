# manage.py


import os
import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()

from project.server import app, db, models

# testing classes
from project.tests.test_user_model import TestUserModel
from project.tests.test_blacklist_token_model import TestBlacklistTokenModel
from project.tests.test_log import TestLog
from project.tests.test__config import TestDevelopmentConfig, TestTestingConfig, TestProductionConfig
from project.tests.api.test_logout import TestLogoutBlueprint
from project.tests.api.test_login import TestLoginBlueprint
from project.tests.api.test_register import TestRegisterBlueprint
from project.tests.api.test_user import TestUserBlueprint

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.option('-c', '--class', dest='test_class', default='all')
def test(test_class):
    """Runs the unit tests without test coverage.
       If given a class name, will only run tests from that class"""
    if test_class == 'all':
        tests = unittest.TestLoader().discover('project/tests')
    else:
        # note, test module must be imported above, doing lazily for now
        test_module = globals()[test_class]
        tests = unittest.TestLoader().loadTestsFromTestCase(test_module)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.option('-c', '--class', dest='test_class', default='all')
def cov(test_class):
    """Runs the unit tests with coverage.
       If given a class name, will determine coverage from that class"""
    if test_class == 'all':
        tests = unittest.TestLoader().discover('project/tests')
    else:
        # note, test module must be imported above, doing lazily for now
        test_module = globals()[test_class]
        tests = unittest.TestLoader().loadTestsFromTestCase(test_module)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()

from project.server.models import User
@manager.command
def t():
    """free form code"""
    user = User.query.filter_by(username="v").first()
    print("username is: " + user.username)

if __name__ == '__main__':
    manager.run()
