import unittest 
import json
from flask import Flask
from app.models import Users, Businesses, Reviews
from app import app, db
from .test_base import BaseTestCase

class ReviewsTestcase(BaseTestCase):
    '''Test for class user'''
    def test_post_reviews(self):
        response = self.post_review()
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Review Posted")
    
    def test_post_reviews_own_business(self):
        self.register_user()
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        
        response = self.app().post("/api/v2/businesses/1/reviews",
                                data=json.dumps(self.review),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Cannot Review your own Business")

    def test_post_review_no_business(self):
        self.register_user()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses/1/reviews",
                                data=json.dumps(self.review),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Cannot Review. Resource(Business) Not Found")   

    def test_get_reviews(self):
        self.register_user()
        self.register_business()
        self.post_review()
        response = self.app().get("/api/v2/businesses/1/reviews",
                                headers = {
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 200)

    def test_get_reviews_no_reviews(self):
        self.register_user()
        self.register_business()
        response = self.app().get("/api/v2/businesses/1/reviews",
                                headers = {
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"No reviews yet.Please review business")

    def test_get_reviews_no_business(self):
        response = self.app().get("/api/v2/businesses/1/reviews",
                                headers = {
                                    "Content-Type": "application/json"
                                })

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Resource(Business) Not Found")