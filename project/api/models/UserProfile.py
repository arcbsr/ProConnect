from email.policy import default
from django.db import models
from rest_framework import serializers
from sqlalchemy import false
from django.contrib.auth.models import User
from .RoleModel import Role
from django.contrib import admin


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True,related_name='role')
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    category = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

def __str__(self):
        return self.name



class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name','role')

 