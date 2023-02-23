from itertools import chain
import itertools
import operator

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
from .permissions import IsAdminAuthenticated, IsProjectAuthor, IsContributor, IsIssueAuthor, IsCommentAuthor, IsValidePkContributor, IsValidePkIssue


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

    # Serializer and queryset
    serializer_class = ProjectSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # Safe method permissions
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        # Other method permissions
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated & (IsProjectAuthor | IsContributor)]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated & IsProjectAuthor]
        else:
            permission_classes=[IsAuthenticated & IsAdminAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Returns the queryset used for this view.
        """
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            # Return only the requested project
            return Project.objects.filter(id=self.kwargs['pk'])
        else:
            # Return all projects
            return Project.objects.all()

    # returns all projects which you are the author or contributor
    def list(self, request, *args, **kwargs):

        # if user isn't contributor, effect filter just on project
        try:
            contributor = Contributor.objects.get(user=self.request.user)
            queryset = Project.objects.filter(Q(author_user = self.request.user) | Q(contributor_project = contributor )).distinct()
        except:
            queryset = Project.objects.filter(author_user = self.request.user)

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

    # Serializer and queryset
    serializer_class = ContributorSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # Safe method permissions
        if self.action == 'list':
            permission_classes = [IsAuthenticated & (IsProjectAuthor | IsContributor)]
        # Other method permissions
        elif  self.action == 'retrieve':
            permission_classes = [IsAuthenticated & IsValidePkContributor & (IsProjectAuthor | IsContributor)]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated & IsProjectAuthor & IsValidePkContributor]
        else:
            permission_classes=[IsAuthenticated & IsAdminAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Returns the queryset used for this view.
        """
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return Contributor.objects.filter(id=self.kwargs.get('pk'))
        else:
            # Return all projects
            project_id = self.kwargs['project_pk']
            return Contributor.objects.filter(project = project_id)

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
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


class IssueViewset(ModelViewSet):

    # Serializer and queryset
    serializer_class = IssuesSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # safe method
        if self.action in ['list', 'create']:
            permission_classes = [IsAuthenticated & (IsContributor | IsProjectAuthor)]
        # other method
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated & IsValidePkIssue & (IsContributor | IsProjectAuthor)]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated & IsIssueAuthor]
        else:
            permission_classes=[IsAuthenticated & IsAdminAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Returns the queryset used for this view.
        """
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return Issue.objects.filter(id=self.kwargs.get('pk'))
        else:
            # Return all projects
            project_id = Issue.objects.filter(project=self.request.resolver_match.kwargs.get('project_pk'))
            return project_id

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        print(type(self.paginate_queryset(self.get_queryset())))
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

    # Serializer and queryset
    serializer_class = CommentsSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # safe method
        if self.action == 'list':
            permission_classes = [IsAuthenticated & ( IsProjectAuthor | IsContributor)]
        # other
        elif self.action == 'create':
            permission_classes = [IsAuthenticated & ( IsProjectAuthor | IsContributor)]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated & IsCommentAuthor]
        else:
            permission_classes=[IsAuthenticated & IsAdminAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Returns the queryset used for this view.
        """
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return Comments.objects.filter(id=self.kwargs.get('pk'))
        else:
            # Return all projects
            issue_id = self.request.resolver_match.kwargs.get('issue_pk')
            return Comments.objects.filter(issue__id = issue_id).order_by('-created_time')

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
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
