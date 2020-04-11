from application import app, db
import flask
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key = True )
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), unique = True , nullable = False)
    pwd = db.Column(db.String(), nullable = False)

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name,
        self.last_name = last_name,
        self.email = email
    
    def set_password(self, pwd):
        self.pwd = generate_password_hash(pwd)
    
    def get_password(self, pwd):
        return check_password_hash(self.pwd, pwd)