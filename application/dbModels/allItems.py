from application import db

class AllItems(db.Model):
    __tablename__ = "allitems"

    item_id = db.Column(db.Integer, primary_key = True )
    user_id = db.Column(db.Integer)
    first_name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    caption = db.Column(db.String(50))
    timestamp = db.Column(db.TIMESTAMP)
    image_path = db.Column(db.String(50))