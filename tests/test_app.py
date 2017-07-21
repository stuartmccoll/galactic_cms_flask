import unittest

from application.init_app import app
from application.views import show_admin


class TestApp(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_show_admin(self):
        with app.test_request_context():
            # Test that the application returns a redirect
            # response when a user is not logged in
            response = show_admin()
            self.assertEqual(response.status_code, 302)

            #


if __name__ == '__main__':
    unittest.main()
