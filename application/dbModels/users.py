from flask_login import UserMixin
from application import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model, UserMixin):
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
    
    @staticmethod
    def isCredentialsCorrect(email, password):
        user = db.session.query(Users).filter(Users.email == email).first()
        if user and user.get_password(password):
            return True, user
        return False, None

    def get_id(self):
        return str(self.user_id)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
