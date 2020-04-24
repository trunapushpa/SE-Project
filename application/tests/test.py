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

        self.assertEqual(app.debug, False)

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

    def register(self, first_name, last_name, email, password, confirmPassword):
        return self.app.post(
            '/register',
            data=dict(first_name=first_name, last_name=last_name, email=email, password=password,
                      confirmPassword=confirmPassword),
            follow_redirects=True
        )

    def test_user_registration_form_displays(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign up', response.data)

    def test_valid_user_registration(self):
        self.app.get('/register', follow_redirects=True)
        random_email = ''.join(random.choices(string.ascii_lowercase, k=8)) + '@' + ''.join(
            random.choices(string.ascii_lowercase, k=8)) + '.com'
        response = self.register('admin', 'admin', random_email, '12345678', '12345678')
        self.assertIn(b'You are successfully registered', response.data)

    def test_duplicate_email_user_registration_error(self):
        self.register('admin', 'admin', 'c@c.com', '12345678', '12345678')
        response = self.register('admin', 'admin', 'c@c.com', '12345678', '12345678')
        self.assertIn(b'Email already registered, Please user another!!', response.data)

    def test_user_profile_without_logging_in(self):
        response = self.app.get('/userprofile')
        self.assertEqual(response.status_code, 401)

    def test_password_and_confirmPassword_error(self):
        response = self.register('admin', 'admin', 'c@c.com', '12345678', '123456789')
        self.assertIn(b'Field must be equal to password.', response.data)


if __name__ == "__main__":
    unittest.main()
