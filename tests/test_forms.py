import unittest
from mock import patch

from application.init_app import app, init_app
from application.forms.login import LoginForm


class MockUser():
    def __init__(self):
        self._query = MockQuery()

    def query(self):
        return self._query


class MockQuery():
    def __init__(self):
        self._filter_by = MockFilter()

    def filter_by(self):
        return self._filter_by


class MockFilter():
    def __init__(self):
        self._first = MockItem()

    def first(self):
        return self._first


class MockItem():
    def __init__(self):
        self.username = 'neilarmstrong'
        self.password = 'password'
        self._validate_login = True

    def validate_login(self, password, another_password):
        return self._validate_login


class MockUserNoReturn():
    def __init__(self):
        self._query = MockBadQuery()

    def query(self):
        return self._query


class MockBadQuery():
    def __init__(self):
        self._filter_by = MockBadFilter()

    def filter_by(self, username):
        return self._filter_by


class MockBadFilter():
    def __init__(self):
        self._first = None

    def first(self):
        return self._first


class MockBadFilterWithReturn():
    def __init__(self):
        self._first = MockBadItem()

    def first(self):
        return self._first


class MockBadItem():
    def __init__(self):
        self.username = 'neilarmstrong'
        self.password = 'password'
        self._validate_login = None

    def validate_login(self, password, another_password):
        return self._validate_login


class TestForms(unittest.TestCase):
    def setUp(self):
        self.app = app
        init_app(self.app)
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    @patch('application.forms.login.FlaskForm.validate')
    @patch('application.forms.login.User')
    def test_validate_fail(self, mock_model, mock_flask_form_validate):
        form = LoginForm()
        form.username.data = 'neilarmstrong'
        form.password.data = 'password'

        mock_flask_form_validate.return_value = False
        form_validate = form.validate()
        self.assertFalse(form_validate)

    @patch('application.forms.login.FlaskForm.validate')
    @patch('application.forms.login.User.query.filter_by')
    @patch('application.forms.login.User.query')
    @patch('application.forms.login.User')
    def test_no_user(self, mock_model, mock_model_query, mock_model_filter_by,
                     mock_flask_form_validate):
        form = LoginForm()
        form.username.data = 'neilarmstrong'
        form.username.errors = list()
        form.password.data = 'password'

        mock_flask_form_validate.return_value = True
        mock_model_filter_by.return_value = MockBadFilter()

        form_validate = form.validate()
        self.assertFalse(form_validate)
        self.assertIn('Invalid login credentials provided',
                      str(form.username.errors))
        self.assertIn('Please try again', str(form.username.errors))

    @patch('application.forms.login.FlaskForm.validate')
    @patch('application.forms.login.User.query.filter_by')
    @patch('application.forms.login.User.query')
    @patch('application.forms.login.User')
    def test_false_validate_login(self, mock_model, mock_model_query,
                                  mock_model_filter_by, 
                                  mock_flask_form_validate):
        form = LoginForm()
        form.username.data = 'neilarmstrong'
        form.username.errors = list()
        form.password.data = 'password'

        mock_flask_form_validate.return_value = True
        mock_model_filter_by.return_value = MockBadFilterWithReturn()

        form_validate = form.validate()
        self.assertFalse(form_validate)
        self.assertIn('Invalid login credentials', str(form.username.errors))

    @patch('application.forms.login.FlaskForm.validate')
    @patch('application.forms.login.User.query.filter_by')
    @patch('application.forms.login.User.query')
    @patch('application.forms.login.User')
    def test_successful_path(self, mock_model, mock_model_query,
                             mock_model_filter_by, mock_flask_form_validate):
        form = LoginForm()
        form.username.data = 'neilarmstrong'
        form.username.errors = list()
        form.password.data = 'password'

        mock_flask_form_validate.return_value = True
        mock_model_filter_by.return_value = MockFilter()

        form_validate = form.validate()
        self.assertTrue(form_validate)
