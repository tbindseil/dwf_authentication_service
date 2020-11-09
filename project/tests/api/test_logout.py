from project.server.log import WARN

import json
import time

from project.tests.base import BaseTestCase
from project.server.models import User, BlacklistToken
from project.server import db
from unittest.mock import patch, MagicMock

class TestLogoutBlueprint(BaseTestCase):
    resp_login = None

    def setUp(self):
        BaseTestCase.setUp(self)

        with self.client:
            # user registration
            resp_register = self.register_user(email='joe@gmail.com', password='123456')

            # user login
            self.resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data_login = json.loads(self.resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(self.resp_login.content_type == 'application/json')
            self.assertEqual(self.resp_login.status_code, 200)

    def test_valid_logout(self):
        """ Test for logout before token expires """
        with self.client:
            # valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        self.resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_logout_no_header(self):
        with self.client:
            response = self.client.post(
                '/auth/logout'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 403)

    @patch('project.server.db.session')
    def test_logout_exception_thrown(self, mock_session):
        with self.client:
            msg = "msg"
            mock_session.commit = MagicMock()
            mock_session.commit.side_effect = Exception(msg)

            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        self.resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == msg, "data['message'] is: " + data['message'])
            self.assertEqual(response.status_code, 200)


    def test_invalid_logout(self):
        """ Testing logout after the token expires """
        with self.client:
            # expire time is 5 seconds in testing only, ow 7 days
            time.sleep(6)
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        self.resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)


    def test_valid_blacklisted_token_logout(self):
        """ Test for logout after a valid token gets blacklisted """
        with self.client:
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(self.resp_login.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            # blacklisted valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        self.resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)
