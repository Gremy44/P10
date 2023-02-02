from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Project, User, Issue, Comments, Contributor
import logging
 
class IsAdminAuthenticated(BasePermission):
 
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

class IsAuthorAuthenticated(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author_user == request.user

class IsAuthorOrContributorProject(BasePermission):
    def has_permission(self, request, view):
    
        # check if author (=> 1 is author, => 0 isn't)
        project = Project.objects.filter(author_user_id=request.user)

        # sort un queryset de tous les projets ou l'user a été trouvé
        is_contributor = Contributor.objects.filter(user_id=request.user)

        return (bool(project.count()>0)) or (bool(is_contributor.count()>0))

    def has_object_permission(self, request, view, obj):
        is_contributor = Contributor.objects.filter(user=request.user, project=obj).count()
        return (bool(request.user == obj.author_user)) or (bool(is_contributor > 0))

class IsAuthorProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (bool(request.user == obj.author_user))

class IsAuthorProjectContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_author = Project.objects.filter(author_user=request.user).count()
        return bool(is_author>0)

class IsAuthorOrContributorIssue(BasePermission):
    def has_permission(self, request, view):
        project_id = request.resolver_match.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        is_contributor = Contributor.objects.filter(user=request.user, project__id=project_id).count()
        return (request.user == project.author_user) or (is_contributor > 0)

    def has_object_permission(self, request, view, obj):
        is_contributor = Contributor.objects.filter(user=request.user, project=obj).count()
        return (request.user == obj.author_user) or (is_contributor > 0)


class IsAuthorIssue(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author_user)

# and obj.permission == 'authorized'
# Seulement Création ou lecture pour les contributeurs sur les commentaires relatifs à un problème
class IsAuthorComment(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.author_user)

class IsAuthorOrContributorComment(BasePermission):
    def has_permission(self, request, view):
        project_id = request.resolver_match.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        is_contributor = Contributor.objects.filter(user=request.user, project__id=project_id).count()
        return (request.user == project.author_user) or (is_contributor > 0)

    def has_object_permission(self, request, view, obj):
        is_contributor = Contributor.objects.filter(user=request.user, project=obj).count()
        return (request.user == obj.author_user) or (is_contributor > 0)