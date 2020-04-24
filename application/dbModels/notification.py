import json
from datetime import datetime, time

from application import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))