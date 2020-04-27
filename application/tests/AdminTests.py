import unittest
import config
from application import app, db
import config
from config import TestingConfig
from flask_login import current_user
from flask.helpers import url_for

class AdminTests(unittest.TestCase):
    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config.from_object(TestingConfig)
        app.config['TESTING'] = True
        app.config['LOGIN_DISABLED'] = True
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
    
    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )
    
    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )
    
    def browseRoute(self, route):
        return self.app.get(
            route, follow_redirects=True
        )
    
    ###############
    #### tests ####
    ###############

    def test_admin_login(self):
        response = self.login("testadmin@a.com", "LS1setup!")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin', response.data)
    
    def test_nonadmin_login(self):
        response = self.login("b@b.com", "12345678")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Admin', response.data)

    def test_nonadminuser_admin_route_access(self):
        with self.app.session_transaction() as session:
            session['user_id'] = 1
            session['first_name'] = 'Mock'
            session['last_name'] = 'user'
            session['email'] = 'mockuser@mock.com'
            session['isadmin'] = False
            session['_fresh'] = True
            response = self.browseRoute("/allusers")
            self.assertIn(b'/home', response.data)
    
    def test_adminuser_admin_route_access(self):
        with self.app.session_transaction() as session:
            session['user_id'] = 1
            session['first_name'] = 'Mock'
            session['last_name'] = 'user'
            session['email'] = 'mockuser@mock.com'
            session['isadmin'] = True
            session['_fresh'] = True
            response = self.browseRoute("/allusers")
            self.assertIn(b'/allusers', response.data)
    
    def test_current_ctx(self):
        with self.app:
            response = self.login("testadmin@a.com", "LS1setup!")
            self.assertEqual(current_user.email, 'testadmin@a.com')

if __name__ == "__main__":
    unittest.main()