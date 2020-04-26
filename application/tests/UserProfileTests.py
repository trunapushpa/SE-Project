import random
import string
import unittest

import config
from application import app, db


class UserProfileTests(unittest.TestCase):

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

    def register(self, first_name, last_name, email, password, confirmPassword):
        return self.app.post(
            '/register',
            data=dict(first_name=first_name, last_name=last_name, email=email, password=password,
                      confirmPassword=confirmPassword),
            follow_redirects=True
        )

    def test_user_profile_page(self):
        self.app.get('/register', follow_redirects=True)
        random_email = ''.join(random.choices(string.ascii_lowercase, k=8)) + '@' + ''.join(
            random.choices(string.ascii_lowercase, k=8)) + '.com'
        self.register('admin', 'admin', random_email, '12345678', '12345678')
        response = self.app.get('/userprofile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Profile', response.data)
        self.assertIn(b'Update Name', response.data)

    def test_user_profile_without_logging_in(self):
        response = self.app.get('/userprofile')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Error!!!', response.data)

if __name__ == "__main__":
    unittest.main()
