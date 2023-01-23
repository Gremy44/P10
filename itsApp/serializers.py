from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from .models import User, Project, Contributor

class UserSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields =['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProjectSerializer(HyperlinkedModelSerializer):

    author_user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']

    def create(self, validated_data):
        validated_data['author_user_id'] = self.context['request'].user.id
        return super().create(validated_data)

class ContributorSerializer(NestedHyperlinkedModelSerializer):

    parent_lookup_kwargs = {
        'project_pk': 'project__pk',
    }

    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Contributor
        fields = ['user_id', 'project_id', 'permission', 'role']

    def create(self, validated_data):
        validated_data['project_id'] = self.context['request'].parser_context['kwargs']['project_pk']
        return super().create(validated_data)

class IssuesSerializer(NestedHyperlinkedModelSerializer):
    pass