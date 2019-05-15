from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)


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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
