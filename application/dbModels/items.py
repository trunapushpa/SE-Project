from datetime import datetime

from application import app, db
from flask import session
import flask


class Items(db.Model):
    __tablename__ = 'items'

    item_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    image_path = db.Column(db.String(50), unique=True, nullable=False)
    caption = db.Column(db.String(50), unique=True, nullable=False)
    feature_vector = db.Column(db.ARRAY(db.FLOAT), nullable=False)

    def __init__(self, tag, location, caption, featurevector):
        self.item_id = '8',
        self.user_id = '1',
        self.type = tag,
        self.location = location,
        self.caption = caption,
        self.image_path = app.config['UPLOAD_FOLDER'],
        self.feature_vector = featurevector



