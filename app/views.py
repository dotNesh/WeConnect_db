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
        
