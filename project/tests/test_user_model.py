import unittest
from unittest.mock import patch, MagicMock
import jwt

from project.server import db
from project.server.models import User, BlacklistToken
from project.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):
    user = None

    def setUp(self):
        BaseTestCase.setUp(self)
        self.user = User(
            username='test@test.com',
            password='test'
        )
        db.session.add(self.user)
        db.session.commit()


    def test_encode_auth_token(self):
        auth_token = self.user.encode_auth_token(self.user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        auth_token = self.user.encode_auth_token(self.user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8")) == 1)

    @patch('project.server.models.BlacklistToken.check_blacklist')
    def test_decode_auth_token_blacklisted_token(self, mock_check_blacklist):
        is_blacklisted_token = True

        mock_check_blacklist.return_value = is_blacklisted_token

        auth_token = self.user.encode_auth_token(self.user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8")) ==
                        "Token blacklisted. Please log in again.")

    @patch('jwt.decode')
    def test_decode_auth_token_expired_token(self, mock_decode):
        mock_decode.side_effect = jwt.ExpiredSignatureError

        auth_token = self.user.encode_auth_token(self.user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8")) ==
                        "Signature expired. Please log in again.")

    @patch('jwt.decode')
    def test_decode_auth_token_invalid_token(self, mock_decode):
        mock_decode.side_effect = jwt.InvalidTokenError

        auth_token = self.user.encode_auth_token(self.user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8")) ==
                       "Invalid token. Please log in again.")


if __name__ == '__main__':
    unittest.main()
