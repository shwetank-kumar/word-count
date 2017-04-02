from wordcounter import db
from sqlalchemy.dialects.postgresql import JSON

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    redis_id = db.Column(db.String())
    ts = db.Column(db.DateTime(timezone=True))
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, redis_id, result_all, result_no_stop_words, ts):
        self.url = url
        self.redis_id = redis_id
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words
        self.ts = ts

    def __repr__(self):
        return '<id {}>'.format(self.id)
