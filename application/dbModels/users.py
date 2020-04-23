from flask_login import UserMixin
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

from application.dbModels.message import Messages
from application.dbModels.notification import Notification


class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    pwd = db.Column(db.String(), nullable=False)
    isadmin = db.Column(db.Boolean)
    messages_sent = db.relationship('Messages',
                                    foreign_keys='Messages.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Messages',
                                        foreign_keys='Messages.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

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

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Messages.query.filter_by(recipient=self).filter(
            Messages.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n
