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

    def register(self, first_name, last_name, email, password, confirmPassword):
        print("here")
        return self.app.post(
            'register/',
            data=dict(first_name=first_name, last_name=last_name, email=email, password=password,
                      confirmPassword=confirmPassword),
            follow_redirects=True
        )

    # def test_user_registration_form_displays(self):
    #     response = self.app.get('/register')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Sign up', response.data)

    # def test_valid_user_registration(self):
    #     self.app.get('/register', follow_redirects=True)
    #     response = self.register('admin', 'admin', 'c@c.com', '12345678', '12345678')
    #     print(response.status_code)
    #     self.assertIn(b'You are successfully registered', response.data)

    # def test_duplicate_email_user_registration_error(self):
    #     self.app.get('/register', follow_redirects=True)
    #     res = self.register('admin', 'admin', 'c@c.com', '12345678', '12345678')
    #     self.app.get('/register', follow_redirects=True)
    #     response = self.register('admin', 'admin', 'c@c.com', '12345678', '12345678')
    #     print(res)
    #     # self.assertIn(b'Email already registered, Please user another!!', response.data)

    # def test_user_profile_without_logging_in(self):
    #     response = self.app.get('/userprofile')
    #     self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()
