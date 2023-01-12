from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Project
import logging
 
class IsAdminAuthenticated(BasePermission):
 
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

class IsAuthorAuthenticated(BasePermission):

    def has_object_permission(self, request, view, obj):
        
        return obj.author_user_id == request.user