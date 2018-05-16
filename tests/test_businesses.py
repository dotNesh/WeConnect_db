import unittest 
import json
from flask import Flask
from app.models import Users, Businesses
from app import app, db
from .test_base import BaseTestCase

class BusinessTestcase(BaseTestCase):    
    def test_add_business(self): 
        response = self.register_business()
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg,"Andela. Business successfully registered by nina")
    
    def test_business_name_empty(self):
        '''Test for blank business name'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                 data=json.dumps(dict(business_name="", category="software",
                                                      location="Nairobi",
                                                      description="This is Andela")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['business_name-Error:']["message"], "business_name cannot be an empty string")

    def test_category_empty(self):
        '''Test for blank category'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                 data=json.dumps(dict(business_name="Andela", category="",
                                                      location="Nairobi",
                                                      description="This is Andela")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['category-Error:']["message"], "category cannot be an empty string")

    def test_location_empty(self):
        '''Test for blank location'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                 data=json.dumps(dict(business_name="Andela", category="software",
                                                      location="", description="This is Andela")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['location-Error:']["message"], "location cannot be an empty string")

    def test_description_empty(self):
        '''Test for blank description'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                 data=json.dumps(dict(business_name="Andela", category="software",
                                                      location="Nairobi", description="")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['description-Error:']["message"], "description cannot be an empty string")

    def test_business_name_none(self):
        '''Test for business name none'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                 data=json.dumps(dict(category="software",
                                                      location="Nairobi",
                                                      description="This is Andela")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['business_name-Error:']["message"], "business_name cannot be missing")

    def test_category_none(self):
        '''Test for category none'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                 data=json.dumps(dict(business_name="Andela",
                                                      location="Nairobi",
                                                      description="This is Andela")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['category-Error:']["message"], "category cannot be missing")

    def test_location_none(self):
        '''Test for location none'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                 data=json.dumps(dict(business_name="Andela", category="software",
                                                     description="This is Andela")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['location-Error:']["message"], "location cannot be missing")

    def test_description_none(self):
        '''Test for description none'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                 data=json.dumps(dict(business_name="Andela", category="software",
                                                      location="Nairobi")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['description-Error:']["message"], "description cannot be missing")


    def test_add_unauthorized_if_no_token_passed(self):
        
        response = self.app().post("/api/v2/businesses",
                                data=json.dumps(self.business),
                                headers = {
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 401)

    def test_existing_business_name(self):
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                data=json.dumps(self.business),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg,"Business Name Taken!")

    def test_get_businesses(self):
        '''test get all businesses'''
        self.register_business()
        response = self.app().get("/api/v2/businesses",
                                    headers = {
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 200)

    def test_get_businesses_if_none(self):
        '''test get all businesses'''
        response = self.app().get("/api/v2/businesses",
                                    headers = {
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['message'],"No businesses yet") 

    def test_get_one_business(self):
        self.register_business()
        response = self.app().get("/api/v2/businesses/1",
                                    headers = {
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['1']['Business name'],"Andela") 

    def test_business_not_found(self):
        response = self.app().get("/api/v2/businesses/1",
                                    headers = {
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Resource Not Found")

    def test_business_update(self):
        response = self.update_business()
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Successfully Updated")

    def test_business_update_not_owner(self):
        self.register_user()
        self.register_business()
        self.register_user2()
        self.access_token = json.loads(self.login_user2().data.decode())['token']

        response = self.app().put("/api/v2/businesses/1",
                                data=json.dumps(self.update),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"You cannot update a business that is not yours")

    def test_business_update_not_found(self):
        self.register_user()
        self.access_token = json.loads(self.login_user().data.decode())['token']

        response = self.app().put("/api/v2/businesses/1",
                                data=json.dumps(self.update),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Cannot Update. Resource(Business) Not Found")

    def test_business_delete(self):
        response = self.delete_business()  
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Successfully Deleted")

    def test_business_delete_not_owner(self):
        self.register_user()
        self.register_business()
        self.register_user2()
        self.access_token = json.loads(self.login_user2().data.decode())['token']

        response = self.app().delete("/api/v2/businesses/1",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })  
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"You cannot delete a business that is not yours")
        
    def test_business_delete_not_found(self):
        self.register_user()
        self.access_token = json.loads(self.login_user().data.decode())['token']

        response = self.app().delete("/api/v2/businesses/1",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })  
        
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Cannot Delete. Resource(Business) Not Found")

    def test_business_search(self):
        response = self.filter_business()

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["1"]["Business name"],"Andela")

    def test_business_filter(self):
        response = self.search_business()

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["1"]["Business name"],"Andela")
        

