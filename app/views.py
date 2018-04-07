'''Contains API Routes'''
from flask import Flask, jsonify, request, make_response
from datetime import datetime
from app.models import Users, Businesses, Reviews
from werkzeug.security import check_password_hash
from app import app


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
