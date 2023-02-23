from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Project, Issue, Comments, Contributor
from django.db.models import Q

 
class IsAdminAuthenticated(BasePermission):
    """
    Verify if is admin authentified
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsProjectAuthor(BasePermission):
    """
    Verify if the user is the creator of project
    """
    def has_permission(self, request, view):
        project_id = request.resolver_match.kwargs.get('project_pk')
        pk = request.resolver_match.kwargs.get('pk')
        if project_id == None:
            project = Project.objects.filter(Q(author_user=request.user) & Q(id=pk))
            print('is_autor_1 : ', bool(project.count()>0))
            return bool(project.count()>0)
        project = Project.objects.filter(Q(author_user=request.user) & Q(id=project_id))
        return bool(project.count()>0)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
    
        
class IsContributor(BasePermission):
    """
    Verify if the user is a contributor of project
    """
    def has_permission(self, request, view):
        project_id= request.resolver_match.kwargs.get('project_pk')
        is_contributor = Contributor.objects.filter(Q(user=request.user) & Q(project=project_id))
        return bool(is_contributor.count() > 0)
        
    def has_object_permission(self, request, view, obj):
        is_contributor = Contributor.objects.filter(Q(user=request.user) & Q(project=obj.project_id))
        return bool(is_contributor.count() > 0)
        

class IsIssueAuthor(BasePermission):
    """
    Verify if the user is the author of the issue
    """
    def has_permission(self, request, view):
        project_id= request.resolver_match.kwargs.get('project_pk')
        author = Issue.objects.filter(Q(author_user=request.user) & Q(project=project_id))
        return bool(author.count()>0)

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author_user)


class IsCommentAuthor(BasePermission):
    """
    Verify if the user is the author of the comment
    """
    def has_object_permission(self, request, view, obj):
        issue_id = request.resolver_match.kwargs.get('issue_id')
        author = Comments.objects.filter(Q(author_user = request.user) & Q(issue_id=issue_id))
        return bool(author.count() > 0) 
    
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.author_user)

class IsValidePkContributor(BasePermission):
    """
    verify if the pk of the request is valid for the request
    """
    def has_object_permission(self, request, view, obj):
        pk_id = request.resolver_match.kwargs.get('pk')
        project_id= request.resolver_match.kwargs.get('project_pk')
        pk_ok = Contributor.objects.filter(Q(id = pk_id) & Q(project=project_id))
        return bool(pk_ok.count())

class IsValidePkIssue(BasePermission):
    """
    verify if the pk of the request is valid for the request
    """
    def has_object_permission(self, request, view, obj):
        pk_id = request.resolver_match.kwargs.get('pk')
        project_id= request.resolver_match.kwargs.get('project_pk')
        pk_ok = Issue.objects.filter(Q(id = pk_id) & Q(project=project_id))
        return bool(pk_ok.count())

