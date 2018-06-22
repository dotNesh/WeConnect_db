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

    def check_password(self, password):
        '''Check Password'''
        return check_password_hash(self.password,password)

    @staticmethod
    def reset_password(username, password):
        '''Reset Password'''
        person = Users.query.filter_by(username=username).first()
        person.password = generate_password_hash(password)
        person.create_user()
               
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

    def serialize(self):
        return {'business_id':self.id,
                'business_name': self.business_name,
                'category': self.category,
                'location': self.location,
                'description': self.description       
        }

    def register_business(self):
        '''Register a Business'''
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(page, limit):
        '''Get all the businesses'''
        subquery = Businesses.query
        offset = (page - 1)*limit
        subquery = subquery.limit(limit).offset(offset)
        
        return subquery.all()
    
    @staticmethod
    def search(data_name, category, location, page, limit):
        '''Search'''
        subquery = Businesses.query
        
        if data_name is not None:
            bizname = "%"+data_name+"%"
            subquery = subquery.filter(Businesses.business_name.ilike(bizname))
        if category is not None:
            subquery = subquery.filter_by(category=category)
        if location is not None:
            subquery = subquery.filter_by(location=location)

        offset = (page - 1)*limit
        subquery = subquery.limit(limit).offset(offset)
        return subquery.all()

    @staticmethod
    def get_one(business_id):
        '''Get a specific business'''
        business = Businesses.query.filter_by(id=business_id).first()
        return business
        
    @staticmethod
    def update_business(business_id,data):
        '''Update a business'''
        business = Businesses.query.filter_by(id=business_id).first()

        if 'category' in data.keys():
            business.category = data['category']
        if 'location' in data.keys():
            business.location = data['location'] 
        if 'description' in data.keys():
            business.description = data['description'] 

        business.register_business()

    @staticmethod
    def delete_business(business_id):
        '''Delete a Business'''
        business = Businesses.query.filter_by(id=business_id).first()
        if business:
            db.session.delete(business)
            db.session.commit()        

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

    def serialize(self):
        return {
                'id': self.id,
                'title': self.title,
                'description': self.description,
                'Reviewer':self.reviewer.username,
                'Business':self.business.business_name
        } 

    def add_review(self):
        '''Add a review'''
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_reviews(business_id):
        '''Get all Reviews'''
        bizreviews = Reviews.query.filter_by(business_id=business_id).all()
        return bizreviews
           