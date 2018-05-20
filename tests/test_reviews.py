import unittest 
import json
from .test_base import BaseTestCase

class ReviewsTestcase(BaseTestCase):
    '''Test for class user'''
    def test_post_reviews(self):
        '''test one can post reviews'''
        response = self.post_review()
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Review Posted")

    def test_post_reviews_description_none(self):
        '''test if description can be missing'''
        self.register_business()
        self.register_user2()
        self.access_token = json.loads(self.login_user2().data.decode())['token']
        response = self.app().post("/api/v2/businesses/1/reviews",
                                data=json.dumps(dict(title="Noma Sana")),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['description-Error:']['message'],
                                      "description cannot be missing")

    def test_post_reviews_title_none(self):
        '''test if title can be missing'''
        self.register_business()
        self.register_user2()
        self.access_token = json.loads(self.login_user2().data.decode())['token']
        response = self.app().post("/api/v2/businesses/1/reviews",
                                data=json.dumps(dict(description="Noma Sana")),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['title-Error:']['message'],
                                      "title cannot be missing")

    def test_post_reviews_description_empty(self):
        '''test if description can be empty'''
        self.register_business()
        self.register_user2()
        self.access_token = json.loads(self.login_user2().data.decode())['token']
        response = self.app().post("/api/v2/businesses/1/reviews",
                                data=json.dumps(dict(title="Noma Sana", description="")),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['description-Error:']['message'],
                                      "description cannot be an empty string")

    def test_post_reviews_title_empty(self):
        '''test if title can be empty'''
        self.register_business()
        self.register_user2()
        self.access_token = json.loads(self.login_user2().data.decode())['token']
        response = self.app().post("/api/v2/businesses/1/reviews",
                                data=json.dumps(dict(title="", description="Noma")),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['title-Error:']['message'],
                                      "title cannot be an empty string")
    
    def test_post_reviews_own_business(self):
        '''Test a business owner can't post a review on their business'''
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
        '''test post review where there is no business'''
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
        '''test get reviews'''
        self.register_user()
        self.register_business()
        self.post_review()
        response = self.app().get("/api/v2/businesses/1/reviews",
                                headers = {
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 200)

    def test_get_reviews_no_reviews(self):
        '''test get reviews when none is posted'''
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
        '''test get reviews where there is no business'''
        response = self.app().get("/api/v2/businesses/1/reviews",
                                headers = {
                                    "Content-Type": "application/json"
                                })

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Resource(Business) Not Found")
