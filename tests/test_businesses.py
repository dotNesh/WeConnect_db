import unittest 
import json
from flask import Flask
from app.models import Users, Businesses
from app import app, db

class BusinessTestcase(unittest.TestCase):
    '''Test for class user'''
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres17!@localhost/weconnect_test'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
        self.app = app.test_client 
        db.init_app(app)
        with app.app_context():
            db.drop_all()
            db.create_all()  

        self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="nina@live",username="nina",
                                password="12345678")), content_type="application/json") 

        self.login_user = self.app().post("/api/v2/auth/login",
                        data=json.dumps(dict(username="nina",password="12345678")),
                                         content_type="application/json") 
      
        self.access_token = json.loads(self.login_user.data.decode())['token']                                       
        
        self.app().post("/api/v2/businesses",
                                data=json.dumps(dict(
                                    business_name="Andela",
                                    category="software",
                                    location="Nairobi",
                                    description="This is Andela",
                                    owner_id="1")),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.dict = dict(
                    business_name="Mutura",
                    category="Food & Drinks",
                    location="Nairobi",
                    description="Tamu Sana",
                    owner_id="1")    
   
    def test_add_business(self): 
        response = self.app().post("/api/v2/businesses",
                                data=json.dumps(self.dict),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg,"Mutura. Business successfully registered")

    def test_add_unauthorized_if_no_token_passed(self):
        
        response = self.app().post("/api/v2/businesses",
                                data=json.dumps( self.dict),
                                headers = {
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 401)

    def test_existing_business_name(self):
        response = self.app().post("/api/v2/businesses",
                                data=json.dumps(dict(
                                    business_name="Andela",
                                    category="software",
                                    location="Nairobi",
                                    description="This is Andela",
                                    owner_id="2")),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg,"Business Name Taken!")   