import unittest
from mock import patch

from application.init_app import app, init_app, db
from application.models.user import User


class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = app
        init_app(self.app)
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_user_model(self):
        user = User('name', 'email', 'pass')
        self.assertEqual(user.username, 'name')
        self.assertEqual(user.email, 'email')
        self.assertEqual(user.password, 'pass')
        self.assertEqual(repr(user),
                         '<User: id=None, username=name, email=email>')
