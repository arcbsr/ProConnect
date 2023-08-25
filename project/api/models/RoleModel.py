from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib import admin



class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200,null=True,blank=True)
    # Add other fields as needed
    def __str__(self):
        return self.name

class RoleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
    list_per_page = 5