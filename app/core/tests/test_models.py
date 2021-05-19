from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_sample_user(email="test@test.com", password="purple_plug_11"):
    """Create a smaple suer"""
    return get_user_model().objects.create_user(email,password)

class ModelTests(TestCase):

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

    def test_tag_str(self):
        """Test tag string representation"""
        tag = models.Tag.objects.create(
            user = create_sample_user(),
            name = 'Blahblahblah'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=create_sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    