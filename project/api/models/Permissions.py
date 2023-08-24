from rest_framework import permissions

class IsEmployer(permissions.BasePermission):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
    def has_permission(self, request, view):
        return True
    
class IsOwner(permissions.BasePermission):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
    def has_permission(self, request, view):
        return request.user.id == 2