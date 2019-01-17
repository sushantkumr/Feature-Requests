# project/test_basic.py

import unittest
from server import app
import json


class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def signup(self, username, password, confirm, client):
        return self.app.post(
            '/signup',
            data=json.dumps(dict(username=username, password=password, confirm=confirm, client=client)),
            follow_redirects=True, mimetype='application/json'
        )

    def login(self, username, password):
        return self.app.post(
            '/login',
            data=json.dumps(dict(username=username, password=password)),
            follow_redirects=True, mimetype='application/json'
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def test_home_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.app.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_user_signup(self):
        response = self.signup('cesar', '123456789012', '123456789012', {"id": 3, "name": "Client C", "$order":8})
        self.assertEqual(response.status_code, 200)

    def test_valid_user_login(self):
        self.signup('cesar', '123456789012', '123456789012', {"id": 3, "name": "Client C", "$order":8})
        response = self.login('cesar', '123456789012')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
