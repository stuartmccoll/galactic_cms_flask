import json
import mock
import unittest

from application.init_app import app, init_app, db
from application.models.user import User
from application.views import get_latest_post, get_latest_posts, \
                              get_next_post, get_previous_post, \
                              page_not_found
import application.views # noqa


class MockItem():
    def __init__(self):
        self.id = 1
        self.title = 'Test Post'
        self.content = 'Content.'
        self.featured_image = 'Featured image'


class MockLimit():
    def __init__(self):
        self._all = {
            MockItem()
        }

    def all(self):
        return self._all


class MockOrderBy():
    def __init__(self):
        self._filter_by = MockFilter()
        self._first = MockItem()
        self._limit = MockLimit()

    def filter_by(self, id, user_id=None):
        return self._filter_by

    def first(self):
        return self._first

    def limit(self, number):
        return self._limit


class MockFilter():
    def __init__(self):
        self._count = 1
        self._first = MockItem()

    def first(self):
        return self._first


class MockPosts():
    def __init__(self):
        self._query = MockQuery()

    def query(self):
        return self._query


class MockQuery():
    def __init__(self):
        self._filter_by = MockFilter()
        self._filter = MockFilter()
        self._order_by = MockOrderBy()

    def filter_by(self, id, user_id=None):
        return self._filter_by

    def filter(self, id):
        return self._filter

    def order_by(self, id, user_id=None):
        return self._order_by


class MockQueryNoReturn():
    def __init__(self):
        self._filter_by = MockBadFilter()
        self._order_by = MockBadOrderBy()

    def filter_by(self, id, user_id=None):
        return self._filter_by

    def order_by(self, id, user_id=None):
        return self._order_by


class MockBadFilter():
    def __init__(self):
        self._count = 0
        self._first = None

    def first(self):
        return self._first


class MockBadOrderBy():
    def __init__(self):
        self._filter_by = MockBadFilter()
        self._first = None
        self._limit = MockBadLimit()

    def filter_by(self, id, user_id=None):
        return self._filter_by

    def first(self):
        return self._first

    def limit(self, id):
        return self._limit


class MockBadLimit():
    def __init__(self):
        self._all = None

    def all(self):
        return self._all


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

    def test_delete_post(self):
        with self.client.session_transaction() as sess:
            # Test that the application returns a redirect
            # response when a user is not logged in
            response = self.client.get('/admin/delete-post/1')
            self.assertEqual(response.status_code, 302)

            sess['user_id'] = 1

        response = self.client.get('/admin/delete-post/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Post deleted successfully')

    @mock.patch('application.views.db.session.query')
    def test_get_edit_post(self, mock_session_query):
        with self.client.session_transaction() as sess:
            # Test that the application returns a redirect
            # response when a user is not logged in
            response = self.client.get('/admin/edit-post/1')
            self.assertEqual(response.status_code, 302)

            sess['user_id'] = 1

        mock_session_query.return_value = MockQuery()

        response = self.client.get('admin/edit-post/1')
        self.assertEqual(response.status_code, 200)

    @mock.patch('application.views.PostForm.validate_on_submit')
    @mock.patch('application.views.db.session.query')
    def test_post_edit_post(self, mock_session_query, mock_validate):
        with self.client.session_transaction() as sess:
            # Test that the application returns a redirect
            # response when a user is not logged in
            response = self.client.post('/admin/edit-post/1')
            self.assertEqual(response.status_code, 302)

            sess['user_id'] = 1

        mock_session_query.return_value = MockQuery()
        mock_validate.return_value = True

        response = self.client.post('/admin/edit-post/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Post updated successfully')

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

    @mock.patch('application.views.db.session.query')
    def test_get_latest_posts(self, mock_session_query):
        mock_session_query.return_value = MockQuery()

        response = json.loads(get_latest_posts(1))
        self.assertEqual(response['1'], 'Test Post')

        mock_session_query.return_value = MockQueryNoReturn()

        response = json.loads(get_latest_posts(1))
        self.assertEqual(response['latest_posts'], False)

    @mock.patch('application.views.db.session.query')
    def test_get_latest_post(self, mock_session_query):
        mock_session_query.return_value = MockQuery()

        response = json.loads(get_latest_post())
        self.assertEqual(response['latest_post'], 1)

        mock_session_query.return_value = MockQueryNoReturn()
        response = json.loads(get_latest_post())
        self.assertEqual(response['latest_post'], False)

    @mock.patch('application.views.Posts.query.filter')
    @mock.patch('application.views.Posts.query')
    @mock.patch('application.views.Posts')
    def test_get_next_post(self, mock_posts, mock_query, mock_filter):
        # Test for the return of a successful response
        mock_filter.return_value = MockFilter()

        response = json.loads(get_next_post(1))
        self.assertEqual(response['next_post'], 1)

        # Test for the return of a non-successful response
        mock_filter.return_value = MockBadFilter()

        response = json.loads(get_next_post(1))
        self.assertEqual(response['next_post'], False)

    @mock.patch('application.views.Posts.query.filter')
    @mock.patch('application.views.Posts.query')
    @mock.patch('application.views.Posts')
    def test_get_previous_post(self, mock_posts, mock_query, mock_filter):
        # Test for the return of a successful response
        mock_filter.return_value = MockFilter()

        response = json.loads(get_previous_post(2))
        self.assertEqual(response['previous_post'], 1)

        # Test for the return of a non-successful response
        mock_filter.return_value = MockBadFilter()

        response = json.loads(get_previous_post(2))
        self.assertEqual(response['previous_post'], False)

    def test_404_response(self):
        response = self.client.get('/does-not-exist')
        self.assertIn('404 Not Found', response.data)
        self.assertEqual(response.status_code, 404)
