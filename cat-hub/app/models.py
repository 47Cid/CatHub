from app import db
from datetime import datetime
from flask_login import UserMixin
import binascii
import os

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='author', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)
    api_key = db.Column(db.String(64), unique=True, nullable=False, default=lambda: binascii.hexlify(os.urandom(32)).decode('utf-8'))


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class AppSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    greeting_message = db.Column(db.String(255), default='Hello')

    def __repr__(self):
        return f"AppSettings('{self.greeting_message}')"