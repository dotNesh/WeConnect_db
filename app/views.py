'''Contains API Routes'''
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_raw_jwt
from app.models import Users, Businesses, Reviews
from werkzeug.security import check_password_hash
from app import app

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECS'] = ['access']
jwt = JWTManager(app)
blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/api/v2/auth/register', methods=['POST'])
def register_user():
    '''Route to register a user'''
    user_data = request.get_json()
    email = user_data.get('email')
    username = user_data.get('username')
    password = user_data.get('password')

    existing_username = Users.query.filter_by(username=username).first()
    existing_email = Users.query.filter_by(email=email).first()
    if existing_username:
        response = {
            'message':"Username Taken!"
        }
        return make_response(jsonify(response['message'])), 409
    elif existing_email:
        response = {
            'message':"Email Already Exists!"
        }
        return make_response(jsonify(response['message'])), 409
    else:
        new_user = Users(email, username, password)
        new_user.create_user()
        response = {
            'message':"Account successfully registered. Log In to access."
            }
        return make_response(jsonify(response['message'])), 201

@app.route('/api/v2/auth/login', methods=['POST'])
def login():
    '''Route to login a User'''
    login_data = request.get_json()
    username = login_data.get('username')
    password = login_data.get('password')    
    
    existing_user = Users.query.filter_by(username= username).first()
    if existing_user:
        valid_user = existing_user.check_password(password)
        if valid_user:
            access_token = create_access_token(identity=existing_user.id)
            response = {
                'message':'Welcome ' + username + ". Log In Succesful!",
                'token': access_token
                }        
            return make_response(jsonify(response)), 200 

        else:
            response = {
                'message':"Invalid Password!"
                }
            return make_response(jsonify(response['message'])), 401   

    else:
        response = {
        'message':"Non-Existent User!"
        }
        return make_response(jsonify(response['message'])), 404

@app.route('/api/v2/auth/reset-password', methods=['POST'])
def reset():
    '''Route to reset a password'''
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')
    
    existing_username = Users.query.filter_by(username= username).first()
    if existing_username:
        Users.reset_password(username, new_password)
        return jsonify({'message':'Password Reset'}), 201

    else:
        response = {
        'message':"Non-Existent User!"
        }
        return make_response(jsonify(response['message'])), 404         
        
@app.route('/api/v2/auth/logout', methods=['POST'])
@jwt_required
def logout():
    '''Route to logout a user'''
    current_user = get_jwt_identity()
    dump = get_raw_jwt()['jti']
    blacklist.add(dump)
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/v2/businesses', methods=['POST'])
@jwt_required
def register_business():
    '''Route to register a business'''
    current_user = get_jwt_identity()
    biz_data = request.get_json()

    business_name = biz_data.get('business_name')
    category = biz_data.get('category')
    location = biz_data.get('location')
    description = biz_data.get('description')

    owner = Users.query.filter_by(id=current_user).first()
    owner_id = owner.id
    existing_business = Businesses.query.filter_by(business_name= business_name).first()
    if existing_business:
        response = {
        'message':"Business Name Taken!"
        }
        return make_response(jsonify(response['message'])), 409

    else:
        new_biz = Businesses(business_name, category, location, description, owner_id)
        new_biz.register_business()
        response = {
            'message': new_biz.business_name + '. Business successfully registered by ' + new_biz.owner.username
            }
        return make_response(jsonify(response['message'])), 201  

@app.route('/api/v2/businesses', methods=['GET'])
def get_business():
    '''Route to get all the businesses'''
    businesses = Businesses.get_all()
    if len(businesses) > 0:
        obj= [business.serialize() for business in businesses]   
        return make_response(jsonify(obj)), 200
    else:
        return jsonify({'message': 'No businesses yet'}), 404

@app.route('/api/v2/businesses/search', methods=['GET'])
def search():
    '''Route to search and filter businesses'''
    data_name = request.args.get('name',type=str)
    data_category = request.args.get('category',type=str)
    data_location = request.args.get('location',type=str)

    businesses = Businesses.search(data_name, data_category, data_location)
    results = {}
    if len(businesses) > 0:
        for business in businesses:
            obj = {business.id:{
                'Business name':business.business_name,
                'Category':business.category,
                'Location':business.location,
                'Created By': business.owner.username,
                'Description':business.description,
                'Created on':business.posted_on
                }
            }
            
            results.update(obj)         
        return make_response(jsonify(results)), 200
    else:
        return jsonify({'message': 'No Match found'}), 404


@app.route('/api/v2/businesses/<int:business_id>', methods=['GET'])   
def get_a_business(business_id):
        business = Businesses.get_one(business_id)
        if business:
            results = {business.id:{
                'Business name':business.business_name,
                'Category':business.category,
                'Location':business.location,
                'Created By': business.owner.username,
                'Description':business.description
                }
            }       
            return make_response(jsonify(results)), 200
        else:
            return jsonify({'message':'Resource Not Found'}), 404

@app.route('/api/v2/businesses/<int:business_id>', methods=['PUT'])
@jwt_required
def update_business(business_id):
    '''Route to update and delete a business'''
    current_user = get_jwt_identity()
    business = Businesses.get_one(business_id)
    if business:
        if current_user == business.owner_id:
            data = request.get_json()
            Businesses.update_business(business_id, data)
            return jsonify({'message':'Successfully Updated'}), 201
        else:
            return jsonify({'message':'You cannot update a business that is not yours'}), 401    

    else:
        return jsonify({'message':'Cannot Update. Resource(Business) Not Found'}), 404 

@app.route('/api/v2/businesses/<int:business_id>', methods=['DELETE'])
@jwt_required
def delete_business(business_id):
    current_user = get_jwt_identity()
    business = Businesses.get_one(business_id)
    if business:
        if current_user == business.owner_id:
            Businesses.delete_business(business_id)
            return jsonify({'message':'Successfully Deleted'}), 201
        else:
            return jsonify({'message':'You cannot delete a business that is not yours'}), 401    

    else:
        return jsonify({'message':'Cannot Delete. Resource(Business) Not Found'}), 404 

@app.route('/api/v2/businesses/<int:business_id>/reviews', methods=['POST'])   
@jwt_required
def reviews(business_id):
    current_user = get_jwt_identity()
    business = Businesses.get_one(business_id)
    if business:
        if current_user != business.owner_id:
            review_data = request.get_json()
            title = review_data.get('title')
            description = review_data.get('description') 
            user_id = business.owner_id
            business_id = business.id

            new_review = Reviews(title, description,user_id,business_id)
            new_review.add_review()
        
            response = {
                        'message': 'Review Posted',
                        }
            return make_response(jsonify(response)), 201
        else:
            return jsonify({'message':'Cannot Review your own Business'}), 401   
    else:
        return jsonify({'message':'Cannot Review. Resource(Business) Not Found'}), 404 

@app.route('/api/v2/businesses/<int:business_id>/reviews', methods=['GET'])  
def get_reviews(business_id): 
    business = Businesses.get_one(business_id)
    if business:    
        allreviews = Reviews.get_reviews(business_id) 
        results = {}
        for allreview in allreviews:
            obj = {allreview.id:{  
            'Business name':business.business_name,      
            'title':allreview.title,
            'Description':allreview.description,   
            'Reviewed by':allreview.reviewer.username   
                }
            }
            results.update(obj)      
        if len(results) > 0:
            return make_response(jsonify(results)), 200
        else:
            return jsonify({'message':'No reviews yet.Please review business'}), 404
    else: 
        return jsonify({'message':'Resource(Business) Not Found'}), 404      



