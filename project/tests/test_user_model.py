import unittest
from unittest.mock import patch, MagicMock
import jwt

from project.server import db
from project.server.models import User
from project.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    @patch('jwt.encode')
    def test_encode_auth_token_throws(self, mock_encode):
        mock_encode.side_effect = Exception

        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()

        output = user.encode_auth_token(user.id)
        assert(output, Exception)

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8")) == 1)

    @patch('jwt.decode')
    def test_decode_auth_token_invalid_token(self, mock_decode):
        mock_decode.side_effect = jwt.InvalidTokenError

        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8")) ==
                       "Invalid token. Please log in again.")

if __name__ == '__main__':
    unittest.main()
