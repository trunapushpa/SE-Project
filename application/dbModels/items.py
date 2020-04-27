from datetime import datetime

from application import db


class Items(db.Model):
    __tablename__ = 'items'

    item_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=False, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now)
    image_path = db.Column(db.String(50), unique=True, nullable=False)
    caption = db.Column(db.String(50), unique=False, nullable=False)
    feature_vector = db.Column(db.ARRAY(db.FLOAT), nullable=False)
    word_vector = db.Column(db.ARRAY(db.FLOAT), nullable=False)
    active = db.Column(db.Boolean, default=True)
    user = db.relationship("Users", backref=db.backref("users", uselist=False))

    def __init__(self, user_id, item_type, location, filename, description, timestamp, feature_vector, word_vector):
        self.user_id = user_id,
        self.type = item_type,
        self.location = location,
        self.filename = filename,
        self.caption = description,
        self.image_path = filename,
        if item_type in ['lost', 'found']:
            self.timestamp = datetime.fromtimestamp(timestamp)
        self.feature_vector = feature_vector
        self.word_vector = word_vector
