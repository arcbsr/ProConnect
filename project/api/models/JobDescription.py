from email.policy import default
from django.db import models
from rest_framework import serializers
from sqlalchemy import false
from django.contrib.auth.models import User


class JobDescription(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    qualifications = models.TextField()
    responsibilities = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
