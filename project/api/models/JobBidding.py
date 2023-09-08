from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin

from api.models import JobDescription

class Bidding(models.Model):
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    worker = models.ForeignKey(User, on_delete=models.CASCADE, default=2)  # Worker who placed the bid
    # job_poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userprofile')  # Job poster
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    submitted_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=True,blank=True)


    def __str__(self):
        return f"{self.worker.username} - ${self.bid_amount}"
    

class BiddingAdmin(admin.ModelAdmin):
    # search_fields = ('title','description')
    list_display = ('id','job','job_author_name','worker','bid_amount')
    list_per_page = 20

    def job_author_name(self, obj):
        return obj.job.author