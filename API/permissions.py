from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Project, User, Issue, Comments, Contributor
from django.db.models import Q
import logging
 
class IsAdminAuthenticated(BasePermission):
 
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsProjectAuthor(BasePermission):

    def has_permission(self, request, view):
        project_id = request.resolver_match.kwargs.get('project_pk')
        if project_id == None:
            project = Project.objects.filter(Q(author_user=request.user) & Q(id=pk))
            print('is_autor_1 : ', bool(project.count()>0))
            return bool(project.count()>0)
        project = Project.objects.filter(Q(author_user=request.user) & Q(id=project_id))
        print('is_autor_2 : ', bool(project.count()>0), ' --- author user : ', request.user.id, ' --- id : ', project_id, ' --- pk : ', request.resolver_match.kwargs.get('pk'))
        return bool(project.count()>0)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
    
        
class IsContributor(BasePermission):
    def has_permission(self, request, view):
        project_id= request.resolver_match.kwargs.get('project_pk')
        is_contributor = Contributor.objects.filter(Q(user=request.user) & Q(project=project_id))
        print('contributeur : ', request.resolver_match.kwargs)
        print('content params : ', request.method)
        return bool(is_contributor.count() > 0)
        
    def has_object_permission(self, request, view, obj):
        is_contributor = Contributor.objects.filter(Q(user=request.user) & Q(project=obj.project_id))
        print('coucou : ', dir(obj))
        return bool(is_contributor.count() > 0)
        

class IsIssueAuthor(BasePermission):
    def has_permission(self, request, view):
        project_id= request.resolver_match.kwargs.get('project_pk')
        author = Issue.objects.filter(Q(author_user=request.user) & Q(project=project_id))
        print("author : ", request.data)
        return bool(author.count()>0)

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author_user)


class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.resolver_match.kwargs)
        issue_id = request.resolver_match.kwargs.get('issue_id')
        author = Comments.objects.filter(Q(author_user = request.user) & Q(issue_id=issue_id))
        print("heheh")
        return bool(author.count() > 0) 
    
    def has_object_permission(self, request, view, obj):
        print("hahaha")
        return bool(request.user == obj.author_user)

class IsValidePkContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        pk_id = request.resolver_match.kwargs.get('pk')
        project_id= request.resolver_match.kwargs.get('project_pk')
        pk_ok = Contributor.objects.filter(Q(id = pk_id) & Q(project=project_id))
        return bool(pk_ok.count())

class IsValidePkIssue(BasePermission):
    def has_object_permission(self, request, view, obj):
        pk_id = request.resolver_match.kwargs.get('pk')
        project_id= request.resolver_match.kwargs.get('project_pk')
        pk_ok = Issue.objects.filter(Q(id = pk_id) & Q(project=project_id))
        return bool(pk_ok.count())

