import random
import string
import unittest

import config
from application import app, db


class ProjectTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = config.Config.SQLALCHEMY_DATABASE_URI
        self.app = app.test_client()
        db.create_all()

        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ########################
    #### helper methods ####
    ########################

    ###############
    #### tests ####
    ###############

    # def test_main_page(self):
    #     response = self.app.get('/', follow_redirects=True)
    #     self.assertIn(b'Some catchy content!', response.data)
    #     self.assertIn(b'Some more catchy content goes here', response.data)

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def register(self, first_name, last_name, email, password, confirmPassword):
        return self.app.post(
            '/register',
            data=dict(first_name=first_name, last_name=last_name, email=email, password=password,
                      confirmPassword=confirmPassword),
            follow_redirects=True
        )

    def test_user_login_form_displays(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_valid_user_login(self):
        self.app.get('/register', follow_redirects=True)
        random_email = ''.join(random.choices(string.ascii_lowercase, k=8)) + '@' + ''.join(
            random.choices(string.ascii_lowercase, k=8)) + '.com'
        self.register('admin', 'admin', random_email, '12345678', '12345678')
        response = self.login(random_email, '12345678')
        self.assertIn(b'Successfully logged in !!', response.data)

    def test_wrong_email_user_login_error(self):
        self.register('admin', 'admin', 'c@c.com', '12345678', '12345678')
        response = self.login('c@c.com', '12345678',)
        self.assertIn(b'Invalid Username or password. Please try again !!', response.data)

    def test_user_profile_without_logging_in(self):
        response = self.app.get('/userprofile')
        self.assertEqual(response.status_code, 500)

if __name__ == "__main__":
    unittest.main()
