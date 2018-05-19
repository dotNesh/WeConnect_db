'''API User Route tests'''
import unittest 
import json
from .test_base import BaseTestCase

class UserTestcase(BaseTestCase):
    '''Test for class user'''            
    def test_create_user(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg,"Account successfully registered. Log In to access.")      

    def test_existing_username(self):
        self.register_user()
        response = self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="kmunene@live.com",username="nina",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['Username-Duplication']['message'],"Username Already Exists!")       

    def test_existing_email(self):
        response = self.register_user()
        response = self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="nina@live.com",username="kmunene",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['Email-Duplication']['message'],"Email Already Exists!")

    def test_email_pattern(self):
        response = self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="nina@live",username="kmunene",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['Email-Format']['message'],"Email format is user@example.com")
    
    def test_password_pattern(self):
        response = self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="ninaa@live.com",username="kmunenee",
                                password="1234")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['Password-Format']['message'],"Must have at least 8 characters")

    def test_new_password_pattern(self):
        self.register_user2()
        response = self.app().post("/api/v2/auth/change-password",
                    data=json.dumps(dict(username="kelvin",old_password="12345678",
                                new_password="1234")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['Password-Format']['message'],"Must have at least 8 characters")


    def test_username_pattern(self):
        response = self.app().post("/api/v2/auth/register",
                    data=json.dumps(dict(email="ninaa@live.com",username="km",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['Username-Format']['message'],"Must have atleast 3 character and no white spaces")        
    
    def test_login(self):
        self.register_user()
        response = self.login_user()

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['message'],"Welcome, Log In Succesful!")
        self.assertTrue(response_msg['token'])

    
    def test_wrong_password(self):
        self.register_user()
        response = self.app().post("/api/v2/auth/login",
                        data=json.dumps(dict(username="nina",password="1234")),
                                         content_type="application/json")

        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg,"Invalid Password!")

    def test_non_existent_user(self):
        response = self.app().post("/api/v2/auth/login",
                        data=json.dumps(dict(username="nina",password="1234")),
                                         content_type="application/json")

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg,"Non-Existent User!")
    
    def test_password_change(self):
        self.register_user()
        response = self.change_password()
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['message'],"Password changed")
        
    def test_login_after_password_change(self):
        self.register_user()
        self.change_password()
        response = self.app().post("/api/v2/auth/login",
                        data=json.dumps(dict(username="nina",password="123645678")),
                                         content_type="application/json")

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Welcome, Log In Succesful!")
        self.assertTrue(response_msg['token'])

    def test_reset_password(self):
        response = self.reset_password()

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Non-existent user. Try signing up")

    def test_reset_password_non_existing(self):
        self.register_user()
        response = self.reset_password()

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"An email has been sent with your new password!")

    def test_password_change_no_user(self):
        response = self.change_password()
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['message'],"Non-Existent User!")

    def test_password_change_wrong_password(self):
        self.register_user()
        response = self.change_password_wrong()
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['message'],"Invalid Password!")
      
    def test_logout_user(self):
        response =  self.logout_user()
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['message'],"Logout successful")

if __name__ == '__main__':
    unittest.main()       
        