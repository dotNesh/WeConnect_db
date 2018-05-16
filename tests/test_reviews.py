import unittest 
import json
from flask import Flask
from app.models import Users, Businesses, Reviews
from app import app, db

class ReviewsTestcase(unittest.TestCase):
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
                    data=json.dumps(dict(email="nina@live.com",username="nina",
                                password="12345678")), content_type="application/json") 

        self.login_user = self.app().post("/api/v2/auth/login",
                        data=json.dumps(dict(username="nina",password="12345678")),
                                         content_type="application/json") 
      
        self.access_token = json.loads(self.login_user.data.decode())['token']

        self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="nesh@live.com",username="nesh",
                                password="12345678")), content_type="application/json") 

        self.login_user2 = self.app().post("/api/v2/auth/login",
                        data=json.dumps(dict(username="nesh",password="12345678")),
                                         content_type="application/json") 
      
        self.access_token2 = json.loads(self.login_user2.data.decode())['token']

        self.app().post("/api/v2/businesses",
                                data=json.dumps( dict(
                                    business_name="Andela",
                                    category="software",
                                    location="Nairobi",
                                    description="This is Andela",
                                    owner_id="1",
                                    owner="nina")),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
    def test_post_reviews(self):
        response = self.app().post("/api/v2/businesses/1/reviews",
                                data=json.dumps(dict(
                                    title="The best",
                                    description="I love being here",
                                    reviewer="nesh",
                                    user_id="2",
                                    business_id="1")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token2),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Review Posted")
    
    def test_post_reviews_own_business(self):
        response = self.app().post("/api/v2/businesses/1/reviews",
                                data=json.dumps(dict(
                                    title="The best",
                                    description="I love being here",
                                    user_id="1",
                                    business_id="1")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Cannot Review your own Business")

    def test_post_review_no_business(self):
        response = self.app().post("/api/v2/businesses/11/reviews",
                                data=json.dumps(dict(
                                    title="The best",
                                    description="I love being here",
                                    user_id="2",
                                    business_id="1")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Cannot Review. Resource(Business) Not Found")   

    def test_get_reviews(self):
        self.app().post("/api/v2/businesses/1/reviews",
                                data=json.dumps(dict(title="The best", description="I love being here",
                                                     user_id="2", business_id="1")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token2),
                                    "Content-Type": "application/json"
                                })

        response = self.app().get("/api/v2/businesses/1/reviews",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        
        print('response', response)

        self.assertEqual(response.status_code, 200)

    def test_get_reviews_no_reviews(self):
        response = self.app().get("/api/v2/businesses/1/reviews",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"No reviews yet.Please review business")

    def test_get_reviews_no_business(self):
        response = self.app().get("/api/v2/businesses/11/reviews",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Resource(Business) Not Found")