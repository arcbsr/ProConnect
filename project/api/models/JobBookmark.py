from django.contrib.auth.models import User
from django.db import models

from api.models import JobDescription

class Bookmark(models.Model):
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Worker who placed the bid
    submitted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username