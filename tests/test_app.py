import unittest

from application.init_app import app, init_app
from application.models.user import User
from application.views import show_admin


class TestApp(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = init_app(app)
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

        User(id=2, username='neilarmstrong', email='neil.armstrong@nasa.gov', password='password')

    # def tearDown(self):
    #     pass

    def test_login(self):
        with self.client:

            self.app.config['WTF_CSRF_ENABLED'] = False

            response = self.client.get("/login")
            self.assertEqual(response.status_code, 200)

            response = self.client.post("/login", data={"username": "neilarmstrong", "password": "password"})
            self.assertEqual(response.location, 200)


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
