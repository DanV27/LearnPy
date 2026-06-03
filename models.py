
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(225), unique = True, nullable = False)
    created_at =  db.Column(db.DateTime, default = datetime.now)
    generations = db.relationship('Generation', backref = 'user')

class Generation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForiegnKey('user.id'), nullable = False)
    spec = db.Column(db.String(500), nullable = False)
    code = db.Column(db.Text, nullable = False)
    test_code = db.Column(db.Text)
    passed = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.now)

