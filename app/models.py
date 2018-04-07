'''Models'''
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Users(db.Model):
    '''Models for table user'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(10000), nullable=False)

    def __init__(self, email, username, password):
        '''Initializes'''
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    