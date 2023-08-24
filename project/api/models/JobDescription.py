from email.policy import default
from django.db import models
from rest_framework import serializers
from sqlalchemy import false
from django.contrib.auth.models import User


class JobDescription(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    keyword = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # User who created the job
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    def __str__(self):
        return self.title
