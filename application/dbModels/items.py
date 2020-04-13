from datetime import datetime

from application import db


class Items(db.Model):
    __tablename__ = 'items'

    item_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    image_path = db.Column(db.String(50), unique=True, nullable=False)
    caption = db.Column(db.String(50), unique=False, nullable=False)
    feature_vector = db.Column(db.ARRAY(db.FLOAT), nullable=False)

    def __init__(self, user_id, item_type, location, filename, description, feature_vector):
        self.user_id = user_id,
        self.type = item_type,
        self.location = location,
        self.filename = filename,
        self.caption = description,
        self.image_path = filename,
        self.feature_vector = feature_vector



