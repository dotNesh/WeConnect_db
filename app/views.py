'''Contains API Routes'''
import uuid
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_raw_jwt
from app.models import Users, Businesses, Reviews
from app import validate
from werkzeug.security import check_password_hash
from flask_mail import Mail, Message 
from app import app


from flask_cors import CORS
CORS(app)

#Mail configurations
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hcravens25@gmail.com'
app.config['MAIL_PASSWORD'] = 'ravens2018'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'hcravens25@gmail.com'
mail = Mail(app)

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
    data = {"username":username,"email":email,"password":password}

    if validate.inputs(data):
        return jsonify(validate.inputs(data)), 406
    
    if validate.pattern(data):
        return jsonify(validate.pattern(data)), 406

    if validate.existing(data):
        return jsonify(validate.existing(data)), 409

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
    
    data = {"username":username, "password":password}
    if validate.inputs(data):
        return jsonify(validate.inputs(data)), 406

    if validate.valid_user(data)['message'] == "Invalid Password!":
        return jsonify(validate.valid_user(data)['message']) , 401
    
    if validate.valid_user(data)['message'] == "Non-Existent User!":
        return jsonify(validate.valid_user(data)['message']) , 404

    else:
        return jsonify(validate.valid_user(data)) , 200


@app.route('/api/v2/auth/change-password', methods=['POST'])
def change_password():
    '''Route to reset a password'''
    data = request.get_json()
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    data = {"username":username,"old_password":old_password,"password":new_password}

    if validate.inputs(data):
        return jsonify(validate.inputs(data)), 406
    
    if validate.pattern(data):
        return jsonify(validate.pattern(data)), 406

    data = {"username":username,"password":old_password,"new_password":new_password}
    if validate.valid_user(data)['message'] == "Welcome, Log In Succesful!":
        Users.reset_password(username, new_password)
        return jsonify({'message':'Password changed'}), 201

    else:
        return jsonify(validate.valid_user(data)) , 401
        

@app.route('/api/v2/auth/reset-password', methods=['POST'])
def reset_password():
    '''Route to change a password'''
    data = request.get_json()
    username = data.get('username')

    existing_username = Users.query.filter_by(username= username).first()
    if existing_username:
        password = str(uuid.uuid4())[:8]
        Users.reset_password(username, password)
        message = Message(
                    subject="Password Reset",
                    sender='hcravens25@gmail.com',
                    recipients=[existing_username.email],
                    body="Hello" + existing_username.username + ",\n Your new password is:" + password
                    )
        mail.send(message)
        return jsonify({'message': 'An email has been sent with your new password!'}), 200

    return jsonify({'message': 'Non-existent user. Try signing up'}), 404

        
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
    
    data = {"business_name":business_name, "category":category, "location":location, "description":description}

    if validate.inputs(data):
        return jsonify(validate.inputs(data)), 406

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
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 2, type=int)
    businesses = Businesses.get_all(page, limit)
    if len(businesses) > 0:
        obj= [business.serialize() for business in businesses]   
        return make_response(jsonify(obj)), 200
    elif len(businesses) == 0 and page == 1:
        return jsonify({'message': 'No businesses yet'}), 404    
    else:
        return jsonify({'message': 'Nothing on this page'}), 200

@app.route('/api/v2/businesses/search', methods=['GET'])
def search():
    '''Route to search and filter businesses'''
    search = request.args.get('q',type=str)
    category = request.args.get('category',type=str)
    location = request.args.get('location',type=str)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 2, type=int)

    businesses = Businesses.search(search, category, location, page, limit)
    if len(businesses) > 0:
        obj = [business.serialize() for business in businesses]
        ctx = {'Businesses':obj,'Current Page':page}     
        return make_response(jsonify(ctx)), 200
    elif len(businesses) == 0 and page == 1:
        return jsonify({'Businesses':{'message': 'No Match found'}}), 404 
    else:
        return jsonify({'Businesses':{'message': 'Nothing on this page'}}), 200


@app.route('/api/v2/businesses/<int:business_id>', methods=['GET'])   
def get_a_business(business_id):
        business = Businesses.get_one(business_id)
        if business:
            results = {
                'Business_id': business.id,
                'Business name':business.business_name,
                'Category':business.category,
                'Location':business.location,
                'Created By': business.owner.username,
                'Description':business.description
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
            data = {"title":title, "description":description}
            if validate.inputs(data):
                return jsonify(validate.inputs(data)), 406
            user_id = business.owner_id
            business_id = business.id
            new_review = Reviews(title, description,user_id,business_id)
            new_review.add_review()
            response = {'message': 'Review Posted',}
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
        obj= [allreview.serialize() for allreview in allreviews]      
        if len(obj) > 0:
            return make_response(jsonify(obj)), 200
        else:
            return jsonify({'message':'No reviews yet.Please review business'}), 404
    else: 
        return jsonify({'message':'Resource(Business) Not Found'}), 404      

