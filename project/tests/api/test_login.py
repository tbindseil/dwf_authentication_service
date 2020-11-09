from project.server.log import WARN

import json

from project.tests.base import BaseTestCase
from unittest.mock import patch

from project.server.models import User

class TestLoginBlueprint(BaseTestCase):
    user_login_data = None

    def setUp(self):
        BaseTestCase.setUp(self)
        self.user_login_data = json.dumps(dict(
            email='joe@gmail.com',
            password='123456'
        ))

    def test_login_succeeds_when_input_valid(self):
        with self.client:
            # user registration
            resp_register = self.register_user(email='joe@gmail.com', password='123456')

            # registered user login
            response = self.client.post(
                '/auth/login',
                data=self.user_login_data,
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_login_fails_for_non_registered_user_login(self):
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=self.user_login_data,
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_login_fails_when_exception_during_login(self):
        with self.client:
            # user registration
            resp_register = self.register_user(email='joe@gmail.com', password='123456')

            with patch("project.server.models.User.encode_auth_token") as mock_encode_auth_token:
                mock_encode_auth_token.side_effect = Exception

                # registered user login
                response = self.client.post(
                    '/auth/login',
                    data=self.user_login_data,
                    content_type='application/json'
                )
                data = json.loads(response.data.decode())
                self.assertTrue(data['status'] == 'fail')
                self.assertTrue(data['message'] == 'Try again')
                self.assertTrue(response.content_type == 'application/json')
                self.assertEqual(response.status_code, 500)
