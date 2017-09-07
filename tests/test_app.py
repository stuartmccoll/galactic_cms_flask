import json
import mock
import unittest

from application.init_app import app, init_app, db
from application.models.user import User
import application.views # noqa


class MockItem():
    def __init__(self):
        self.id = 1


class MockFilter():
    def __init__(self):
        self._count = 0
        self._first = MockItem()

    def first(self):
        return self._first


class MockQuery():
    def __init__(self):
        self._filter_by = MockFilter()

    def filter_by(self, id):
        return self._filter_by


class TestApp(unittest.TestCase):
    def setUp(self):

        # creates a test client
        self.app = app
        init_app(self.app)
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.debug = False
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

        get_test_user = db.session.query(User) \
            .filter_by(username='neilarmstrong').first()

        if get_test_user is None:
            test_user = User(username='neilarmstrong',
                             email='neil.armstrong@nasa.gov',
                             password='pbkdf2:sha256:50000$rX'
                             + 'R42TlH$d6d360487f2d858caec323'
                             + '2065c3daa408d15f1bdb7278ce343'
                             + 'fb60993f5c3dc')
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        self._ctx.pop()

    def test_login(self):
        with self.client:

            response = self.client.get('/login')
            self.assertEqual(response.status_code, 200)

            response = self.client.post('/login', data={'username':
                                        'neilarmstrong', 'password':
                                                         'protect'})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location,
                             'http://localhost/admin/dashboard')

            response = self.client.post('/login', data={'username':
                                        'neilarmstrong', 'password':
                                                        'protect'},
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            response = self.client.post('/login', data={'username':
                                        'neilarmstrong', 'password':
                                                         'invalid'})
            self.assertIn('Invalid login credentials provided', response.data)
            self.assertIn('Please try again', response.data)

    def test_home(self):
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_show_admin(self):
        with self.client.session_transaction() as sess:
            # Test that the application returns a redirect
            # response when a user is not logged in
            response = self.client.get("/admin/dashboard")
            self.assertEqual(response.status_code, 302)

            # Test that the application returns a 200
            # response when a user is logged in
            sess['user_id'] = 1
            sess['_fresh'] = True

        response = self.client.get("/admin/dashboard")
        self.assertEqual(response.status_code, 200)

    # def test_create_post(self):
    #     with self.client.session_transaction() as sess:
    #         # Test that the application returns a redirect
    #         # response when a user is not logged in
    #         response = self.client.get('/admin/create-post')
    #         self.assertEqual(response.status_code, 302)

    #         response = self.client.post('/admin/create-post')
    #         self.assertEqual(response.status_code, 302)

    #         sess['user_id'] = 1
    #         sess['_fresh'] = True

    #     response = self.client.get('/admin/create-post')
    #     self.assertEqual(response.status_code, 200)

    #     response = self.client.post('/admin/create-post',
    #                                 data={'title': 'Test Post'})
    #     response_json = json.loads(response.data)
    #     self.assertEqual(response_json['status'], 'failure')

    #     response = self.client.post('/admin/create-post',
    #                                 data={'content': 'Test Content'})
    #     response_json = json.loads(response.data)
    #     self.assertEqual(response_json['status'], 'failure')

    # def test_create_post_2(self):
    #     with self.client.session_transaction() as sess:
    #         sess['user_id'] = 1
    #         sess['_fresh'] = True

    #     with mock.patch('application.views.base64.b64encode') as mock_base64encode, \
    #             mock.patch('application.views.PostForm') as mock_form:
    #         mock_base64encode.return_value = "Image"
    #         mock_form.return_value.title.return_value.data.return_value = "hello"
    #         response = self.client.post('/admin/create-post',
    #                                     data={'title': 'Test Post',
    #                                         'content': 'Test content',
    #                                         'featured_image': 'Image'})
    #         self.assertEqual(response.status_code, 200)

    def test_view_posts(self):
        with self.client.session_transaction() as sess:
            # Test that the application returns a redirect
            # response when a user is not logged in
            response = self.client.get('/admin/view-posts')
            self.assertEqual(response.status_code, 302)

            sess['user_id'] = 1

        response = self.client.get('/admin/view-posts')
        self.assertEqual(response.status_code, 200)

    @mock.patch('application.views.get_latest_posts')
    @mock.patch('application.views.get_latest_post')
    @mock.patch('application.views.get_next_post')
    @mock.patch('application.views.get_previous_post')
    @mock.patch('application.views.db.session.query')
    def test_view_post(self, mock_session_query, mock_get_previous_post,
                       mock_get_next_post, mock_get_latest_post,
                       mock_get_latest_posts):
        mock_session_query.return_value = MockQuery()
        mock_get_previous_post.return_value = json.dumps({"previous_post": 1})
        mock_get_next_post.return_value = json.dumps({"next_post": 2})
        mock_get_latest_post.return_value = json.dumps({"latest_post": 3})
        mock_get_latest_posts.return_value = json.dumps({"latest_posts": 1})

        response = self.client.get('/post/1')
        self.assertEqual(response.status_code, 200)

    def test_user_settings(self):
        with self.client.session_transaction() as sess:
            # Test that the application returns a redirect
            # response when a user is not logged in
            response = self.client.get('/admin/user-settings')
            self.assertEqual(response.status_code, 302)

            response = self.client.post('/admin/user-settings')
            self.assertEqual(response.status_code, 302)

            sess['user_id'] = 1

        response = self.client.get('/admin/user-settings')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/admin/user-settings')
        response_json = json.loads(response.data)
        self.assertEqual(response_json['status'], 'failure')

        response = self.client.post('/admin/user-settings',
                                    data={'first_name': 'Neil',
                                          'last_name': 'Armstrong'})
        self.assertEqual(response.data, 'User settings updated successfully')
        self.assertEqual(response.status_code, 200)
