from django.contrib import admin

from api.models import Category, Image
from api.models import JobBidding, JobBookmark
from .models import UserProfile, JobDescription, RoleModel
from .models.JobDescription import JobDescriptionAdmin
from .models.UserProfile import UserProfileAdmin
from .models.RoleModel import RoleAdmin


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RoleModel.Role,RoleAdmin)
admin.site.register(JobDescription, JobDescriptionAdmin)
admin.site.register(Image)
admin.site.register(Category.Category)
admin.site.register(Category.Type)
admin.site.register(JobBidding.Bidding, JobBidding.BiddingAdmin)




