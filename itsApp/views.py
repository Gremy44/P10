from django.shortcuts import render

from rest_framework.permissions import SAFE_METHODS
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q


from .models import User, Project, Contributor, Issue, Comments
from .serializers import UserSerializer, ProjectSerializer, ContributorSerializer, IssuesSerializer, CommentsSerializer
from .permissions import IsAuthorOrContributorProject, IsAuthorProject, IsAuthorProjectContributor, IsAuthorOrContributorIssue, IsAuthorIssue, IsAuthorComment, IsAuthorOrContributorComment


class UsersViewset(ReadOnlyModelViewSet):
    """ 
    GET : get all users in db
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

class ActualUserView(ModelViewSet):

    queryset = get_user_model().objects.none()
    serializer_class = UserSerializer

    def list(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

class SignupViewset(ModelViewSet):
    """
    POST : create new user
    """

    serializer_class = UserSerializer

    @action(methods=['post'], detail=True)
    def create_user(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewset(ModelViewSet):
    """
    GET/id : get the project with id  
    POST : create new project 
    """

    serializer_class = ProjectSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in SAFE_METHODS:
            permission_classes = [IsAuthenticated & IsAuthorOrContributorProject]
        elif self.action == 'post':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes=[IsAuthenticated & IsAuthorProject]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Project.objects.filter(author_user = self.request.user)

    @action(methods=['post'], detail=True)
    def create_project(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put', 'patch', 'delete'], detail=True)
    def del_put_project(self, request):
        project = Project.objects.all()
        serializer = ProjectSerializer(project, data=request.data)
        return Response(serializer.data)


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in SAFE_METHODS:
            permission_classes = [IsAuthenticated & IsAuthorOrContributorProject]
        elif self.action == 'post':
            permission_classes = [IsAuthenticated & IsAuthorProjectContributor]
        else:
            permission_classes=[IsAuthenticated & IsAuthorProjectContributor]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        project_id = self.request.resolver_match.kwargs.get('project_pk')
        return Contributor.objects.filter(project = project_id)

    @action(methods=['post'], detail=True)
    def create_contributor(self, request, project_id=None):
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put', 'patch', 'delete'], detail=True)
    def del_put_contributor(self, request):
        contributor = Contributor.objects.all()
        serializer = ContributorSerializer(contributor, data=request.data)
        return Response(serializer.data)


class IssueViewset(ModelViewSet):

    serializer_class = IssuesSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in SAFE_METHODS:
            permission_classes = [IsAuthenticated & IsAuthorOrContributorIssue]
        elif self.action == 'post':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorIssue]
        else:
            permission_classes=[IsAuthenticated & IsAuthorIssue]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        project_id = self.request.resolver_match.kwargs.get('project_pk')
        return Issue.objects.filter(project__id = project_id).order_by('-created_time')

    def check_contributor(self, request):
        contributor_list = []
        validation_list = []

        project_id = self.request.resolver_match.kwargs.get('project_pk')
        contributors = Contributor.objects.filter(project=project_id)

        '''for i in contributors:
            if serializer.data'''

        '''for n in contributors.values_list():
            contributor_list.append(n[1])

        for i in contributor_list:
            if i == User.objects.get(pk=request.data):
                validation_list.append(True)
            else: 
                validation_list.append(False)

        if any(validation_list):
            print('ok')
        else:
            raise ValidationError({"message": "Assignee user isn't contributor"})'''

    @action(methods=['post'], detail=True)
    def create_issue(self, request, pk=None):
        serializer = IssuesSerializer(data=request.data)
        if serializer.is_valid():
            validation_list = []
            project_id = self.request.resolver_match.kwargs.get('project_pk')
            contributors = Contributor.objects.filter(project=project_id)
            
            for i in contributors:
                if serializer.data.get('assignee_user_id') == i:
                    validation_list.append(True)
                else:
                    validation_list.append(False)
                    
            if any(validation_list):
                print('ok')
            else:
                raise ValidationError({"message": "Assignee user isn't contributor"})

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put', 'patch', 'delete'], detail=False)
    def del_put_contributor(self, request):
        issue = Issue.objects.all()
        serializer = IssuesSerializer(issue, data=request.data)
        return Response(serializer.data)


class CommentViewset(ModelViewSet):

    serializer_class = CommentsSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in SAFE_METHODS:
            permission_classes = [IsAuthenticated & IsAuthorOrContributorComment]
        elif self.action == 'post':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorIssue]
        else:
            permission_classes=[IsAuthenticated & IsAuthorComment]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        project_id = self.request.resolver_match.kwargs.get('project_pk')
        issue_id = self.request.resolver_match.kwargs.get('issue_pk')

        return Comments.objects.filter(issue__id = issue_id).order_by('-created_time')

    @action(methods=['post'], detail=True)
    def create_comment(self, request, project_id=None):
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put', 'patch', 'delete'], detail=True)
    def del_put_contributor(self, request):
        comment = Comments.objects.all()
        serializer = CommentsSerializer(comment, data=request.data)
        return Response(serializer.data)
