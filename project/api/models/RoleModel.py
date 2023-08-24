from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.models import Token

class Role(models.Model):
    name = models.CharField(max_length=50)
    # Add other fields as needed
