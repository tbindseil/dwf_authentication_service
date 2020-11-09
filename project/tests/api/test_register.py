import unittest
import json

from project.server import db
from project.server.models import User
from project.tests.base import BaseTestCase
from unittest.mock import patch


class TestRegisterBlueprint(BaseTestCase):
    def test_registration_registers_when_input_valid(self):
        with self.client:
            response = self.register_user(email='joe@gmail.com', password='123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_register_fails_with_already_registered_user(self):
        with self.client:
            response = self.register_user(email='joe@gmail.com', password='test')

            response = self.register_user(email='joe@gmail.com', password='123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_register_fails_when_execption_during_register(self):
        with patch("project.server.models.User.encode_auth_token") as mock_encode_auth_token:
            with self.client:
                mock_encode_auth_token.side_effect = Exception

                response = self.register_user(email='joe@gmail.com', password='123456')
                data = json.loads(response.data.decode())
                self.assertTrue(data['status'] == 'fail')
                self.assertTrue(data['message'] == 'Some error occurred. Please try again.')
                self.assertTrue(response.content_type == 'application/json')
                self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
