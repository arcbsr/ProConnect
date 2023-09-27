from django.contrib import admin

from api.models import Category, Image, ProjectStatus
from api.models import JobBidding, JobBookmark
from api.models.CVAnalyzerModel import CV
from .models import UserProfile, JobDescription, RoleModel
from .models.JobDescription import JobDescriptionAdmin
from .models.UserProfile import UserProfileAdmin
from .models.RoleModel import RoleAdmin
from .models.OrderModel import Order


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RoleModel.Role,RoleAdmin)
admin.site.register(JobDescription, JobDescriptionAdmin)
admin.site.register(Image)
admin.site.register(Category.Category)
admin.site.register(Category.Type)
admin.site.register(Order)
admin.site.register(CV)
admin.site.register(Category.Skills)
admin.site.register(JobBidding.Bidding, JobBidding.BiddingAdmin)
admin.site.register(ProjectStatus.ProjectStatus, ProjectStatus.ProjectStatusAdmin)





