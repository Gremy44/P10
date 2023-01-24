from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Project, User, Issue, Comments, Contributor
import logging
 
class IsAdminAuthenticated(BasePermission):
 
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

class IsAuthorAuthenticated(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author_user_id == request.user


# Responsables + contributeurs
class IsAuthorOrContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user or obj.permission == 'authorized')


# Seulement Création ou lecture pour les contributeurs sur les commentaires relatifs à un problème
class ContributorCreateOrRead(BasePermission):
    pass


# Seul l'auteur peut actualiser ou supprimer problème/projet/commentaire
class AuthorPutOrDel(BasePermission):
    pass