import unittest
from unittest.mock import patch, MagicMock

from project.server import db
from project.server.models import User, BlacklistToken
from project.tests.base import BaseTestCase


class TestBlacklistTokenModel(BaseTestCase):
    token_str = 'token'
    blt = None

    def setUp(self):
        BaseTestCase.setUp(self)
        self.blt = BlacklistToken(self.token_str)
        db.session.add(self.blt)
        db.session.commit()

    def test_repr(self):
        outcome = self.blt.__repr__()
        assert(outcome == '<id: token: token')

    def test_check_blacklist_found(self):
        outcome = BlacklistToken.check_blacklist(self.token_str)
        assert(outcome)

    def test_check_blacklist_not_found(self):
        non_blt_token_str = 'non_blt_token_str'
        outcome = BlacklistToken.check_blacklist(non_blt_token_str)
        assert(outcome == False)


if __name__ == '__main__':
    unittest.main()
