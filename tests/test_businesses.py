import unittest 
import json
from .test_base import BaseTestCase

class BusinessTestcase(BaseTestCase):    
    def test_add_business(self):
        '''Test one can add a business'''
        response = self.register_business()
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg,"Andela. Business successfully registered by nina")

    def test_add_unauthorized_if_no_token_passed(self):
        '''Test Unauthorized if no token passed'''
        response = self.app().post("/api/v2/businesses",data=json.dumps(self.business),
                                    headers = {"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 401)

    def test_existing_business_name(self):
        '''Test Existing Business Name'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                data=json.dumps(self.business),headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg,"Business Name Taken!")

    def test_get_businesses(self):
        '''test get all businesses'''
        self.register_business()
        response = self.app().get("/api/v2/businesses?page=1&limit=2",headers = {"Content-Type": "application/json"})

        self.assertEqual(response.status_code, 200)
        

    def test_get_businesses_none_on_page(self):
        '''test get no businesses on page'''
        self.register_business()
        response = self.app().get("/api/v2/businesses?page=2&limit=2",headers = {"Content-Type": "application/json"})

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['message'],"Nothing on this page")

    def test_get_businesses_if_none(self):
        '''test get all businesses'''
        response = self.app().get("/api/v2/businesses",headers = {"Content-Type": "application/json"})
        
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['message'],"No businesses yet") 

    def test_get_one_business(self):
        '''Test can get one business'''
        self.register_business()
        response = self.app().get("/api/v2/businesses/1",headers = {"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['Business name'],"Andela") 

    def test_business_not_found(self):
        '''Test business not found'''
        response = self.app().get("/api/v2/businesses/1",headers = {"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Resource Not Found")

    def test_business_update(self):
        '''Test one can update a business'''
        response = self.update_business()
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Successfully Updated")

    def test_business_update_not_owner(self):
        '''Test only owner can update a business'''
        self.register_business()
        self.register_user2()
        self.access_token = json.loads(self.login_user2().data.decode())['token']
        response = self.app().put("/api/v2/businesses/1",data=json.dumps(self.update),headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"You cannot update a business that is not yours")

    def test_business_update_not_found(self):
        '''Test update on a non-existing business'''
        self.register_user()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().put("/api/v2/businesses/1",data=json.dumps(self.update),headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Cannot Update. Resource(Business) Not Found")

    def test_business_delete(self):
        '''Test one can delete a business'''
        response = self.delete_business()  
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Successfully Deleted")

    def test_business_delete_not_owner(self):
        '''Test only owner can delete a business'''
        self.register_business()
        self.register_user2()
        self.access_token = json.loads(self.login_user2().data.decode())['token']
        response = self.app().delete("/api/v2/businesses/1",headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"})  
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"You cannot delete a business that is not yours")
        
    def test_business_delete_not_found(self):
        '''Test delete on a non-existing business'''
        self.register_user()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().delete("/api/v2/businesses/1",headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"})         
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Cannot Delete. Resource(Business) Not Found")

    def test_business_search(self):
        '''Test Business search'''
        response = self.filter_business()
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["Businesses"][0]["business_name"],"Andela")
    
    def test_business_search_no_match(self):
        '''Test Business search no match'''
        self.register_business()
        response = self.app().get("/api/v2/businesses/search?category=food&location=kenya",
                            headers = {
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["Businesses"]["message"],"No Match found")
    
    def test_business_search_nothing_on_page(self):
        '''Test Business search nothing on page '''
        self.register_business()
        response = self.app().get("/api/v2/businesses/search?category=software&location=Nairobi&page=3&limit=2",
                            headers = {
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["Businesses"]["message"],"Nothing on this page")

    def test_business_filter(self):
        '''Test Business filter'''
        response = self.search_business()
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["Businesses"][0]["business_name"],"Andela")
        

