from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

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

