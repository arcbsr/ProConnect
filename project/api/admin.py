from django.contrib import admin
from .models import UserProfile, JobDescription

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(JobDescription)
