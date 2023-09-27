from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Skills(models.Model):
    name = models.CharField(max_length=100, unique=True)
    course_link = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name