from django.db import models
from django.contrib.auth.models import User

class CV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='cv_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    keywords = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title