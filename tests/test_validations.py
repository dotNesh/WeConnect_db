import unittest 
import json
from .test_base import BaseTestCase

class ValidationTestcase(BaseTestCase):
    '''Test validations'''
    def test_username_none(self):
        response = self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="ninaa@live.com",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['username-Error:']['message'],"username cannot be missing")

    def test_email_none(self):
        response = self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(username="ninaa",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['email-Error:']['message'],"email cannot be missing")

    def test_password_none(self):
        response = self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="ninaa@live.com",
                                username="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['password-Error:']['message'],"password cannot be missing")

    def test_username_blank(self):
        response = self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="nina@live",username="",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['username-Error:']['message'],"username cannot be an empty string")

    def test_email_blank(self):
        response = self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="",username="neshh",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['email-Error:']['message'],"email cannot be an empty string")

    def test_password_blank(self):
        response = self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="nina@live",username="neshhh",
                                password="")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))        
        self.assertEqual(response_msg['password-Error:']['message'],"password cannot be an empty string")

    def test_username_none_login(self):
        response = self.app().post("/api/v2/auth/login",
                        data=json.dumps(dict(password="12345678")),
                                         content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['username-Error:']['message'],"username cannot be missing")

    def test_password_none_login(self):
        response = self.app().post("/api/v2/auth/login",
                        data=json.dumps(dict(username="nina")),
                                         content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['password-Error:']['message'],"password cannot be missing")

    def test_username_blank_login(self):
        response = self.app().post("/api/v2/auth/login",
                        data=json.dumps(dict(username="",password="12345678")),
                                         content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['username-Error:']['message'],"username cannot be an empty string")

    def test_password_blank_login(self):
        response = self.app().post("/api/v2/auth/login",
                        data=json.dumps(dict(username="nesh",password="")),
                                         content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['password-Error:']['message'],"password cannot be an empty string")

    def test_password_change_blank_inputs(self):
        response = self.app().post("/api/v2/auth/change-password",
                        data=json.dumps(dict(username="",new_password="",old_password="")),
                                         content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['old_password-Error:']['message'],"old_password cannot be an empty string")
        self.assertEqual(response_msg['username-Error:']['message'],"username cannot be an empty string")
        self.assertEqual(response_msg['password-Error:']['message'],"password cannot be an empty string")
        
    def test_password_change_missing_inputs(self):
        response = self.app().post("/api/v2/auth/change-password",
                        data=json.dumps(dict()),
                                         content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['old_password-Error:']['message'],"old_password cannot be missing")
        self.assertEqual(response_msg['username-Error:']['message'],"username cannot be missing")
        self.assertEqual(response_msg['password-Error:']['message'],"password cannot be missing")

    def test_business_name_empty(self):
        '''Test for blank business name'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']

        response = self.app().post("/api/v2/businesses",
                                 data=json.dumps(dict(business_name="", category="software",
                                                      location="Nairobi", description="This is Andela")),
                                 headers={"Authorization": "Bearer {}".format(self.access_token),
                                          "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['business_name-Error:']["message"], "business_name cannot be an empty string")

    def test_category_empty(self):
        '''Test for blank category'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']

        response = self.app().post("/api/v2/businesses",
                                 data=json.dumps(dict(business_name="Andela", category="",
                                                      location="Nairobi", description="This is Andela")),
                                 headers={"Authorization": "Bearer {}".format(self.access_token),
                                          "Content-Type": "application/json"})
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
                                 headers={"Authorization": "Bearer {}".format(self.access_token),
                                          "Content-Type": "application/json"})
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
                                 headers={"Authorization": "Bearer {}".format(self.access_token),
                                          "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['description-Error:']["message"], "description cannot be an empty string")

    def test_business_name_none(self):
        '''Test for business name none'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                 data=json.dumps(dict(category="software",location="Nairobi",
                                                      description="This is Andela")),
                                 headers={"Authorization": "Bearer {}".format(self.access_token),
                                          "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['business_name-Error:']["message"], "business_name cannot be missing")

    def test_category_none(self):
        '''Test for category none'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                 data=json.dumps(dict(business_name="Andela",location="Nairobi",
                                                      description="This is Andela")),
                                 headers={"Authorization": "Bearer {}".format(self.access_token),
                                          "Content-Type": "application/json"})
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
                                 headers={"Authorization": "Bearer {}".format(self.access_token),
                                          "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['location-Error:']["message"], "location cannot be missing")

    def test_description_none(self):
        '''Test for description none'''
        self.register_business()
        self.access_token = json.loads(self.login_user().data.decode())['token']
        response = self.app().post("/api/v2/businesses",
                                 data=json.dumps(dict(business_name="Andela", category="software",location="Nairobi")),
                                 headers={"Authorization": "Bearer {}".format(self.access_token),
                                          "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['description-Error:']["message"], "description cannot be missing")

