'''Contains validations'''
import re
from app.models import Users, Businesses, Reviews
from flask_jwt_extended import create_access_token

def existing(data):
    messages = {}
    if 'username' in data.keys():
        ex = Users.query.filter_by(username=data['username']).first()
        if ex:
            message = {"message":"Username Already Exists!"}
            messages.update({"Username-Duplication":message})

    if 'email' in data.keys():
        ex = Users.query.filter_by(email=data['email']).first()
        if ex:
            message = {"message":"Email Already Exists!"}
            messages.update({"Email-Duplication":message})

    return messages

def valid_user(data):
    messages = {}
    if 'username' in data.keys():
        ex = Users.query.filter_by(username=data['username']).first()
        if ex:
            valid_user = ex.check_password(data['password'])
            if valid_user:
                access_token = create_access_token(identity=ex.id)
                message = {'message':'Welcome ' + data['username'] + ". Log In Succesful!",'token': access_token}
                messages.update(message)
            
            else:
                message = {'message':"Invalid Password!"}
                messages.update(message)
        else:
            message = {'message':"Non-Existent User!"}
            messages.update(message)

    return messages
    

def inputs(data):
    messages = {}
    for key in data:
        if data[key] is None:
            message = {'message': key + ' cannot be missing'}
            messages.update({key+'-Error:':message})
        else:   
            blank = re.sub(r'\s+', '', data[key])
            if not blank:
                message = {'message': key + ' cannot be an empty string'}
                messages.update({key+'-Error:':message})
    return messages
            
def pattern(data):
    messages = {}
    if 'email' in data.keys():
        pattern = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",data['email'])
        if not pattern:
           message = {"message":"Email format is user@example.com"}
           messages.update({"Email-Format":message})
    
    if 'password' in data.keys():
        pattern = re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', data['password'])
        if not pattern:
            message = {"message":"Must have at least 8 characters"}
            messages.update({"Password-Format":message})
    if 'username' in data.keys():
        pattern = re.match(r'^[a-zA-Z_]+[\d\w]{3,}', data['username'])
        if not pattern:
            message = {"message":"Must have atleast 3 character and no white spaces"}
            messages.update({"Username-Format":message})
    return messages
    
    