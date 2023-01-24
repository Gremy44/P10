from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.shortcuts import get_object_or_404

from .models import User, Project, Contributor, Issue, Comments
from .serializers import UserSerializer, ProjectSerializer, ContributorSerializer, IssuesSerializer, CommentsSerializer
from .permissions import IsAdminAuthenticated, IsAuthorAuthenticated

class UsersViewset(ReadOnlyModelViewSet):
    """ 
    GET : get all users in db
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

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

    def get_queryset(self):
        return Project.objects.all()

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def create_project(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def get_project(self, request):
        return Project.objects.all()

    @action(methods=['put', 'delete'], detail=True, permission_classes=[IsAuthenticated])
    def del_put_project(self, request):
        project = Project.objects.all()
        serializer = ProjectSerializer(project, data=request.data)
        return Response(serializer.data)

class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def create_contributor(self, request, project_id=None):
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def get_contributor(self, request):
        return Contributor.objects.all()

    @action(methods=['put', 'delete'], detail=True, permission_classes=[IsAuthenticated])
    def del_put_contributor(self, request):
        contributor = Contributor.objects.all()
        serializer = ContributorSerializer(contributor, data=request.data)
        return Response(serializer.data)

class IssueViewset(ModelViewSet):

    serializer_class = IssuesSerializer

    def get_queryset(self):
        return Issue.objects.all()

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def create_issue(self, request, project_id=None):
        serializer = IssuesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def get_issues(self, request):
        return Issue.objects.all()

    @action(methods=['put', 'delete'], detail=True, permission_classes=[IsAuthenticated])
    def del_put_contributor(self, request):
        issue = Issue.objects.all()
        serializer = IssuesSerializer(issue, data=request.data)
        return Response(serializer.data)


class CommentViewset(ModelViewSet):
    
    serializer_class = CommentsSerializer

    def get_queryset(self):
        return Comments.objects.all()

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def create_comment(self, request, project_id=None):
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def get_comments(self, request):
        return Comments.objects.all()

    @action(methods=['put', 'delete'], detail=True, permission_classes=[IsAuthenticated])
    def del_put_contributor(self, request):
        comment = Comments.objects.all()
        serializer = CommentsSerializer(comment, data=request.data)
        return Response(serializer.data)