'''Models'''
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Users(db.Model):
    '''Models for table users'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(10000), nullable=False)
    businesses = db.relationship('Businesses', backref='owner',lazy=True)
    reviews = db.relationship('Reviews', backref='reviewer', lazy=True)

    def __init__(self, email, username, password):
        '''Initializes'''
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
    def create_user(self):
        '''creates a user'''
        db.session.add(self)
        db.session.commit()
class Businesses(db.Model):
    '''Models for table businesses'''

    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviews = db.relationship('Reviews', backref='business', lazy=True)
    posted_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, business_name, category, location, description,owner_id):
        '''Initializes'''
        self.business_name = business_name
        self.category = category
        self.location = location
        self.description = description
        self.owner_id = owner_id   

class Reviews(db.Model):      
    '''Models for table reviews'''

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    posted_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, description,user_id,business_id):
        '''Initializes'''
        self.title = title
        self.description = description  
        self.user_id = user_id
        self.business_id = business_id          