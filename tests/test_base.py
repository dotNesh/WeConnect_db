'''Base Test File'''
import unittest 
import json
from app import app, db

class BaseTestCase(unittest.TestCase):
    '''Base Tests'''
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

        self.user={"username":"nina","email":"nina@live.com","password":"12345678"}
        self.user2={"username":"kelvin","email":"kelvin@live.com","password":"12345678"}
        self.login={"username":"nina","password":"12345678"}
        self.login2={"username":"kelvin","password":"12345678"}
        self.reset={"username":"nina","new_password":"12s45678"}
        self.business={"business_name":"Andela","category":"software","location":"Nairobi",
                        "description":"This is Andela","owner_id":"1"}
        self.update={"category":"Food","location":"Thika","description":"This is America"}
        self.review={"title":"The best","description":"I love being here","reviewer":"nesh",
                    "user_id":"2","business_id":"1"}
    
    def register_user(self):
        response = self.app().post("/api/v2/auth/register",
                    data=json.dumps(self.user), 
                    content_type="application/json")
        return response
    
    def register_user2(self):
        response = self.app().post("/api/v2/auth/register",
                    data=json.dumps(self.user2), 
                    content_type="application/json")
        return response
    
    def login_user(self):
        response = self.app().post("/api/v2/auth/login",
                    data=json.dumps(self.login), 
                    content_type="application/json")
        return response
    
    def login_user2(self):
        response = self.app().post("/api/v2/auth/login",
                    data=json.dumps(self.login2), 
                    content_type="application/json")
        return response
    
    def change_password(self):
        response = self.app().post("/api/v2/auth/reset-password",
                        data=json.dumps(self.reset),
                                         content_type="application/json")
        return response

    def reset_password(self):
        response = self.app().post("/api/v2/auth/change-password",
                        data=json.dumps(dict(username="nina")),
                                         content_type="application/json")
        return response
         
    def logout_user(self):
        self.register_user()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/auth/logout",
            headers = {
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"
                })
        return response
        
    def register_business(self):
        self.register_user()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                data=json.dumps(self.business),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })                        
        return response

    def update_business(self):
        self.register_user()
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().put("/api/v2/businesses/1",
                                data=json.dumps(self.update),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        return response
    
    def delete_business(self):
        self.register_user()
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().delete("/api/v2/businesses/1",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        return response

    def search_business(self):
        self.register_user()
        self.register_business()
        response = self.app().get("/api/v2/businesses/search?q=andela",
                            headers = {
                                    "Content-Type": "application/json"
                                })
        return response
    
    def filter_business(self):
        self.register_user()
        self.register_business()
        response = self.app().get("/api/v2/businesses/search?category=software&location=Nairobi",
                            headers = {
                                    "Content-Type": "application/json"
                                })
        return response
        
        
    def post_review(self):
        self.register_user()
        self.register_business()
        self.register_user2()
        self.access_token = json.loads(self.login_user2().data.decode())['token']
        response = response = self.app().post("/api/v2/businesses/1/reviews",
                                data=json.dumps(self.review),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        return response




        
        

