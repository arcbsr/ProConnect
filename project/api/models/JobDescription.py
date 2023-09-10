from email.policy import default
from django.db import models
from rest_framework import serializers
from sqlalchemy import false
from django.contrib.auth.models import User
from django.contrib import admin

from api.models.Category import Category, Type

class JobDescription(models.Model):
    title = models.CharField(max_length=100,blank=True)
    description = models.TextField(null=True,blank=True)
    keyword = models.TextField(null=True,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)  # User who created the job
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    is_active = models.BooleanField(default=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT,default=1, null=True,blank=True)
    jobtype = models.ForeignKey(Type, on_delete=models.SET_DEFAULT,default=1, null=True,blank=True)
    

    def __str__(self):
        return self.title
    

class JobDescriptionAdmin(admin.ModelAdmin):
    search_fields = ('title','description')
    list_display = ('title','author','description')
    list_per_page = 20
    # readonly_fields= ('start_date','end_date','start_time','end_time')
