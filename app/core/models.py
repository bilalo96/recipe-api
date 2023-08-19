"""Database Model"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    """Manager for user"""
    def create_user(self,email,password=None,**extra_fields):#**extra_field:can provide keyword arguments and usefull when add aditional fields and don't need tp update user model
        """Create,save and retuen a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password):
        """Create and return a new superuser"""
        user=self.create_user(email,password)
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)

        return user

# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):#AbstractBaseUser:functionality for auth system,PermissionsMixin:functionality for permissions
    """User in The System"""
    email=models.EmailField(max_length=254,unique=True)
    name= models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff= models.BooleanField(default=True)

    objects=UserManager()

    USERNAME_FIELD='email' # defines the field that we want to use for authentications

class Recipe(models.Model):
    """Recipe object"""
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='recipe', on_delete=models.CASCADE)
    title= models.CharField(max_length=255)
    description=models.TextField(blank=True)
    time_minutes=models.IntegerField()
    price=models.DecimalField( max_digits=5, decimal_places=2)
    link= models.CharField(max_length=255,blank=True)
    tags=models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

class Tag(models.Model):
    """Tag for filtering recipes"""
    name=models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='tag', on_delete=models.CASCADE)

    def  __str__(self):
         return self.name






