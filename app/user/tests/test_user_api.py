from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the users api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test successful user creation with payload"""
        payload = {
            'email':'blah@blah.net',
            'password':'blahblahblah',
            'name':'blahblahson'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creation of pre-existing user fails"""
        payload = {'email' : 'jamesohgan@gmail.com', 'password' : 'fakepassword_65'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    
    #ADD PW LENGTH TEST
    def test_create_token_for_user(self):
        """Test that a token is created for user"""
        payload = {'email':'test@test.test', 'password':'white_plug_92'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test creating a token without valid credentials"""
        create_user(email="test@test.test", password="white_plug_92")
        payload = {'email':'test@test.test', 'password':'justflatoutincorrect'}
        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email':'test@test.test', 'password':'white_plug_92'}
        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test token isn't created with mssing field"""
        res = self.client.post(TOKEN_URL,{})
        self.assertNotIn("token",res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
