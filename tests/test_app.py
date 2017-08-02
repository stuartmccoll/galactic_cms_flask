import unittest

from application.init_app import app, init_app, db
from application.models.user import User
from application.views import show_admin


class TestApp(unittest.TestCase):
    def setUp(self):

        # creates a test client
        self.app = app
        init_app(self.app)
        self.app.config['WTF_CSRF_ENABLED'] = False
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

    # def tearDown(self):
    #     pass

    def test_login(self):
        with self.client:

            response = self.client.get('/login')
            self.assertEqual(response.status_code, 200)

            response = self.client.post('/login', data={'username': 'neilarmstrong', 'password': 'protect'})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, 'http://localhost/admin/dashboard')

            response = self.client.post('/login', data={'username': 'neilarmstrong', 'password': 'protect'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)


    # def test_show_admin(self):
    #     with self.client:
    #         # Test that the application returns a redirect
    #         # response when a user is not logged in
    #         response = self.client.get("/admin/dashboard")
    #         self.assertEqual(response.status_code, 302)

    #         # Test that the application returns a 200
    #         # response when a user is logged in
    #         with self.client.session_transaction() as sess:

    #             sess['user_id'] = 1
    #             sess['_fresh'] = True

    #             res = self.client.get("/admin/dashboard")
    #             self.assertEqual(res, 'hello')



# if __name__ == '__main__':
#     unittest.main()
