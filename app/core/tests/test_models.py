from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):

    def test_create_user_with_email_success(self):
        """Test creating new user with email"""
        email = 'fake@fake.net'
        password = 'notarealpassword'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test new user email"""
        email = 'fake@Fake.net'
        user  = get_user_model().objects.create_user(email, "test123")

        self.assertEqual(user.email,email.lower())

    def test_new_user_invalid_email(self):
        """Test creating new user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'12345')

    def test_create_new_superuser(self):
        """Test new superuser is created"""
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            '12345'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)