from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token as DefaultToken
        
        
class CustomUser(AbstractUser):
    custom = models.CharField(max_length=500, default='')
    phone = models.CharField(max_length=20, default='')
    street = models.CharField(max_length=150, default='')
    city = models.CharField(max_length=150, default='')
    email_confirmation_token = models.CharField(max_length=50, default='')
    email_confirmed = models.BooleanField(default=False)
    image = models.CharField(max_length=500, default='', null=True)
