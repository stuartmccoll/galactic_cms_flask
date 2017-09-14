import unittest

from application.init_app import app, init_app, db
from application.models.user import User
from application.models.user_profile import UserProfile


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

    def test_user_profile_model(self):
        user_profile = UserProfile(1969, 'Buzz', 'Aldrin')
        self.assertEqual(user_profile.id, 1969)
        self.assertEqual(user_profile.first_name, 'Buzz')
        self.assertEqual(user_profile.last_name, 'Aldrin')
        self.assertEqual(repr(user_profile),
                         '<User Profile : id=1969, first_name=Buzz, ' +
                         'last_name=Aldrin>')
        self.assertEqual(user_profile.full_name(), 'Buzz Aldrin')
