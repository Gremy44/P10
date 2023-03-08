from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSerializer


class UsersViewset(ReadOnlyModelViewSet):
    """
    GET : get all users in db
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()


class ActualUserView(ReadOnlyModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset


class SignupViewset(ModelViewSet):
    """
    POST : create new user
    """

    serializer_class = UserSerializer
    http_method_names = ['post']

    @swagger_auto_schema(methods=['post'], auto_schema=None)
    @action(detail=False, methods=['post'])
    def user_create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
