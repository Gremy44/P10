from django.shortcuts import render
from django.http import Http404
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
from .permissions import IsAuthorOrContributorProject, IsAuthorProject, IsAuthorProjectContributor, IsAuthorOrContributorContributor, IsAuthorOrContributorIssue, IsAuthorIssue, IsAuthorComment, IsAuthorOrContributorComment, IsAdminAuthenticated


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

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in SAFE_METHODS:
            permission_classes = [IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorProject]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorProject]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated & IsAuthorProject]
        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticated & IsAuthorProject]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated & IsAuthorProject]
        else:
            permission_classes=[IsAuthenticated & IsAdminAuthenticated]
        return [permission() for permission in permission_classes]

    # returns all projects which you are the author or contributor
    def list(self, request, *args, **kwargs):
        queryset = Project.objects.filter(Q(author_user = self.request.user) | Q(contributor__user = self.request.user)).distinct()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create new project
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # return project with id
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # update all data
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # update selected data
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # delete project
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {'message': 'ID delete'}
        return Response(data, status=204)


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in SAFE_METHODS:
            permission_classes = [IsAuthenticated & IsAuthorOrContributorContributor]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorContributor]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorContributor]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated & IsAuthorProjectContributor]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated & IsAuthorProjectContributor]
        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticated & IsAuthorProjectContributor]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated & IsAuthorProjectContributor]
        else:
            permission_classes=[IsAuthenticated & IsAdminAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        project_id = self.request.resolver_match.kwargs.get('project_pk')
        queryset = Contributor.objects.filter(project = project_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        project_author = Project.objects.filter(author_user=self.request.user).count()
        serializer = self.get_serializer(data=request.data)
        print(project_author)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {'message': 'ID delete'}
        return Response(data, status=204)


class IssueViewset(ModelViewSet):

    queryset = Issue.objects.all()
    serializer_class = IssuesSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in SAFE_METHODS:
            permission_classes = [IsAuthenticated & IsAuthorOrContributorIssue]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorIssue]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorIssue]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorIssue]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated & IsAuthorIssue]
        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticated & IsAuthorIssue]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated & IsAuthorIssue]
        else:
            permission_classes=[IsAuthenticated & IsAdminAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        project_id = self.request.resolver_match.kwargs.get('project_pk')
        queryset = Issue.objects.filter(project__id = project_id).order_by('-created_time')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {'message': 'ID delete'}
        return Response(data, status=204)


class CommentViewset(ModelViewSet):

    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in SAFE_METHODS:
            permission_classes = [IsAuthenticated & IsAuthorOrContributorComment]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorComment]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorComment]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorComment]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorComment]
        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorComment]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated & IsAuthorOrContributorComment]
        else:
            permission_classes=[IsAuthenticated & IsAdminAuthenticated]
        return [permission() for permission in permission_classes]

    '''def get_permissions(self):
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
'''
    def list(self, request, *args, **kwargs):
        issue_id = self.request.resolver_match.kwargs.get('issue_pk')
        queryset = Comments.objects.filter(issue__id = issue_id).order_by('-created_time')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {'message': 'ID delete'}
        return Response(data, status=204)
