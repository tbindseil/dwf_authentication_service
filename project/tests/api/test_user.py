import json

from project.tests.base import BaseTestCase
from project.server.models import User, BlacklistToken
from project.server import db

class TestUserBlueprint(BaseTestCase):
    resp_register = None

    def setUp(self):
        BaseTestCase.setUp(self)
        self.resp_register = self.register_user(email='joe@gmail.com', password='123456')

    def test_user_status(self):
        """ Test for user status """
        with self.client:
            response = self.client.get(
                '/auth/user',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        self.resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['email'] == 'joe@gmail.com')
            self.assertTrue(data['data']['admin'] is 'true' or 'false')
            self.assertEqual(response.status_code, 200)

    def test_user_status_no_auth_header(self):
        with self.client:
            response = self.client.get(
                '/auth/user'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_user(self):
        """ Test for user status with a blacklisted valid token """
        with self.client:
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(self.resp_register.data.decode())['auth_token'])
            blacklist_token.__repr__()
            db.session.add(blacklist_token)
            db.session.commit()
            response = self.client.get(
                '/auth/user',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        self.resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)
