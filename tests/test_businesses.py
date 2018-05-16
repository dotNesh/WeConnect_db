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
        '''User 1'''
        self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="nina@live.com",username="nina",
                                password="12345678")), content_type="application/json") 

        self.login_user = self.app().post("/api/v2/auth/login",
                        data=json.dumps(dict(username="nina",password="12345678")),
                                         content_type="application/json") 
      
        self.access_token = json.loads(self.login_user.data.decode())['token']  

        '''User 2'''
        self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="ron@live.com",username="ronn",
                                password="12345678")), content_type="application/json") 

        self.login_user2 = self.app().post("/api/v2/auth/login",
                        data=json.dumps(dict(username="ronn",password="12345678")),
                                         content_type="application/json") 
      
        self.access_token2 = json.loads(self.login_user2.data.decode())['token']                                     
        
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
        self.assertEqual(response_msg,"Mutura. Business successfully registered by nina")
    
    def test_business_name_empty(self):
        '''Test for blank business name'''
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
    def test_get_businesses(self):
        '''test get all businesses'''
        response = self.app().get("/api/v2/businesses",
                                    headers = {
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 200)
    def test_get_businesses_if_none(self):
        '''test get all businesses'''
        self.app().delete("/api/v2/businesses/1",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        response = self.app().get("/api/v2/businesses",
                                    headers = {
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['message'],"No businesses yet")     
    def test_get_one_business(self):
        response = self.app().get("/api/v2/businesses/1",
                                    headers = {
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['1']['Business name'],"Andela") 

    def test_business_not_found(self):
        response = self.app().get("/api/v2/businesses/11",
                                    headers = {
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Resource Not Found")
    def test_business_update(self):
        response = self.app().put("/api/v2/businesses/1",
                                data=json.dumps(dict(
                                    category="software development",
                                    location="Kampala",
                                    description="TIA")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Successfully Updated")
    def test_business_update_not_owner(self):
        response = self.app().put("/api/v2/businesses/1",
                                data=json.dumps(dict(
                                    category="software development",
                                    location="Kampala",
                                    description="TIA")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token2),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"You cannot update a business that is not yours")

    def test_business_update_not_found(self):
        response = self.app().put("/api/v2/businesses/11",
                                data=json.dumps(dict(
                                    category="software development",
                                    location="Kampala",
                                    description="TIA")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Cannot Update. Resource(Business) Not Found")
    def test_business_delete(self):
        response = self.app().delete("/api/v2/businesses/1",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })  
        
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Successfully Deleted")
    def test_business_delete_not_owner(self):
        response = self.app().delete("/api/v2/businesses/1",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token2),
                                    "Content-Type": "application/json"
                                })  
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"You cannot delete a business that is not yours")
    def test_business_delete_not_found(self):
        response = self.app().delete("/api/v2/businesses/11",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })  
        
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Cannot Delete. Resource(Business) Not Found")                                      
