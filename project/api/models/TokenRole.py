from knox.models import AuthToken
from django.db import models
 
from api.models.RoleModel import Role

class ExtendedAuthToken(AuthToken):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)