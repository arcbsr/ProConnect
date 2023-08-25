from django.contrib import admin
from .models import UserProfile, JobDescription, RoleModel
from .models.JobDescription import JobDescriptionAdmin
from .models.UserProfile import UserProfileAdmin
from .models.RoleModel import RoleAdmin


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RoleModel.Role,RoleAdmin)
admin.site.register(JobDescription, JobDescriptionAdmin)




