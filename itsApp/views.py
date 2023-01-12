from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.shortcuts import get_object_or_404

from .models import User, Project, Contributor
from .serializers import UserSerializer, ProjectSerializer, ContributorSerializer
from .permissions import IsAdminAuthenticated, IsAuthorAuthenticated
import permissions

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
    permission_classes = [IsAuthenticated,]
    queryset = Project.objects.all()

    def list(self, request, client_pk=None):
        queryset = Project.objects.filter(client=client_pk)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, client_pk=None):
        queryset = Project.objects.filter(pk=pk, client=client_pk)
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

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
    def get_project(self, request):
        print("coucou")
        serializer = ProjectSerializer(object)
        return Response(serializer.data)

class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()
    permission_classes = (permissions.AllowAny,)

    def list(self, request, client_pk=None):
        queryset = Contributor.objects.filter(client=client_pk)
        serializer = ContributorSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, client_pk=None):
        queryset = Contributor.objects.filter(pk=pk, client=client_pk)
        contributor = get_object_or_404(queryset, pk=pk)
        serializer = ContributorSerializer(contributor)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def create_contributor(self, request):
        print('coucou : ', request)
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def get_contributor(self, request):
        return Contributor.objects.all()