from datetime import datetime

from application import db


class WordVector(db.Model):
    __tablename__ = 'word_vector'

    word_id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), nullable=False)
    vector = db.Column(db.ARRAY(db.FLOAT), nullable=False)

    def __init__(self, word, vector):
        self.word = word,
        self.vector = vector
