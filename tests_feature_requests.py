# project/test_basic.py

import unittest

import flask_login
from lib.models import db
from lib.core import config
from flask import Flask


TEST_DB = 'test.db'

configuration = config.CONFIGS['TEST']

app = Flask(__name__)

app.secret_key = configuration['secret_key']
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/signup', follow_redirects=True)
        print(response)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
