from project.server.log import WARN

import json

from project.tests.base import BaseTestCase
from unittest.mock import patch

from project.server.models import User

class TestLoginBlueprint(BaseTestCase):
    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            resp_register = self.register_user(email='joe@gmail.com', password='123456')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_exception_during_login(self):
        with self.client:
            # user registration
            resp_register = self.register_user(email='joe@gmail.com', password='123456')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)

            with patch("project.server.models.User.encode_auth_token") as mock_encode_auth_token:
                mock_encode_auth_token.side_effect = Exception

                # registered user login
                response = self.client.post(
                    '/auth/login',
                    data=json.dumps(dict(
                        email='joe@gmail.com',
                        password='123456'
                    )),
                    content_type='application/json'
                )
                data = json.loads(response.data.decode())
                self.assertTrue(data['status'] == 'fail')
                self.assertTrue(data['message'] == 'Try again')
                self.assertTrue(response.content_type == 'application/json')
                self.assertEqual(response.status_code, 500)
