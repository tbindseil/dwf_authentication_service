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

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.option('-c', '--class', dest='test_class', default='all')
def cov(test_class):
    """Runs the unit tests with coverage.
       If given a class  name, will determine coverage from that class"""
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


if __name__ == '__main__':
    manager.run()
