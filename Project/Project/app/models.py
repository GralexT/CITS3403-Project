from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Comparison(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    subreddit = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(120))
    timescale = db.Column(db.String(120))
    colours = db.Column(db.String(120))

    def __repr__(self):
        return '<Comparison {}>'.format(self.key)