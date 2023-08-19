""" Test for models """
from django.test import TestCase
from django.contrib.auth import get_user_model # helper function to get default user model for the project,and you can referance to the model directly from the models we are difined
from decimal import Decimal
from core import models

def create_user(email='user@example.com',password='testpass123'):
    """Create and retuen a new user"""
    return get_user_model().objects.create_user(email,password)


class ModelTest(TestCase):
    """Test models"""
    def test_create_user_with_email_successful(self):
        """Test creating user with email succesful"""
        email='test@example.com'
        password='testpass123'
        user=get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
    def test_new_user_email_normalized(self):
        """Test email is normalized for new user"""
        sample_emails=[
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@Example.com','Test2@example.com'], # here is T capitel because mail standard
            ['TEST3@EXAMPLE.COM','TEST3@example.com'],
            ['test4@example.COM','test4@example.com'],
        ]
        for email, expected in sample_emails:
              user=get_user_model().objects.create_user(email,'sample123')
              self.assertEqual(user.email,expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without email raises """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')

    def test_create_superuser(self):
        """Test creating superuser"""
        user=get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_create_recipe(self):
        """Test creatig a recipe is successful"""
        user=get_user_model().objects.create_user(  #to sign recipe object
            'test@example.com',
            'testpass123',
        )
        recipe=models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description',
        )
        self.assertEqual(str(recipe),recipe.title)

    def test_create_tag(self):
        """Test creating a Tag"""
        user=create_user()
        tag=models.Tag.objects.create(user=user,name='Tag1')

        self.assertEqual(str(tag),tag.name)
