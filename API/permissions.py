from rest_framework.permissions import BasePermission
from .models import Project, Issue, Contributor, Comments
from django.db.models import Q


class IsAdminAuthenticated(BasePermission):
    """
    Verify if is admin authentified
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsProjectAuthor(BasePermission):
    """
    Verify if the user is the creator of project
    """

    def has_permission(self, request, view):
        project_id = request.resolver_match.kwargs.get('project_pk')
        pk = request.resolver_match.kwargs.get('pk')
        if project_id is None:
            project = Project.objects.filter(
                Q(author_user=request.user) & Q(id=pk))
            return bool(project.count() > 0)
        project = Project.objects.filter(
            Q(author_user=request.user) & Q(id=project_id))
        return bool(project.count() > 0)

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Contributor):
            return bool(request.user == obj.project.author_user)
        return bool(request.user == obj.author_user)


class IsContributor(BasePermission):
    """
    Verify if the user is a contributor of project.
    """

    def has_permission(self, request, view):
        project_id = request.resolver_match.kwargs.get('project_pk')
        if project_id is None:
            project_id = request.resolver_match.kwargs.get('pk')
        is_contributor = Contributor.objects.filter(
            Q(user=request.user) & Q(project=project_id)
        )
        return bool(is_contributor.count() > 0)

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            project_id = obj.id
        else:
            project_id = request.resolver_match.kwargs.get('project_pk')

        if (
            isinstance(obj, Contributor)
            and str(obj.project.id) != str(project_id)
        ):
            return False
        if (
            isinstance(obj, Issue)
            and str(obj.project.id) != str(project_id)
        ):
            return False
        if (
            isinstance(obj, Comments)
            and str(obj.issue.project.id) != str(project_id)
        ):
            return False
        is_contributor = Contributor.objects.filter(
            Q(user=request.user) & Q(project__id=project_id)
        ).count()
        return bool(is_contributor > 0)


class IsIssueAuthor(BasePermission):
    """
    Verify if the user is the author of the issue
    """

    def has_permission(self, request, view):
        project_id = request.resolver_match.kwargs.get('project_pk')
        author = Issue.objects.filter(
            Q(author_user=request.user) & Q(project=project_id))
        return bool(author.count() > 0)

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author_user)


class IsCommentAuthor(BasePermission):
    """
    Verify if the user is the author of the comment
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.author_user)
