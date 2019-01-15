import unittest
import sys
sys.path.append("..")

from app import app, db  # noqa: E402
from app.config import Test  # noqa: E402
from flask_testing import TestCase  # noqa: E402


class AppTest(TestCase):

    def create_app(self):
        app.config.from_object(Test)
        return app

    def setUp(self):
        # app.config.from_object(Test)
        self.app = self.create_app()
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_assert_index_template_used(self):
        render_templates = False
        response = self.app.get('/')
        self.assert_template_used('index.html')
        self.assert_context('clients', [])
        self.assert_context('features', [])

    def test_assert_feature_template_used(self):
        render_templates = False
        response = self.app.get('/features')
        self.assert_template_used('feature.html')
        self.assertTrue(self.get_context_variable('form'))

    def test_assert_client_template_used(self):
        render_templates = False
        response = self.app.get('/clients')
        self.assert_template_used('client.html')
        self.assertTrue(self.get_context_variable('form'))


if __name__ == "__main__":
    unittest.main()
