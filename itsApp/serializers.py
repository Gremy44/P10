from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from .models import User, Project, Contributor, Issue, Comments

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


class ProjectSerializer(ModelSerializer):

    author_user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']

    def create(self, validated_data):
        validated_data['author_user_id'] = self.context['request'].user.id
        return super().create(validated_data)

class ContributorSerializer(ModelSerializer):

    parent_lookup_kwargs = {
        'project_pk': 'project__pk',
    }

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'permission', 'role']

    def create(self, validated_data):
        project_id = self.context['request'].parser_context['kwargs']['project_pk']
        validated_data['project'] = Project.objects.get(pk=project_id)
        return super().create(validated_data)

class IssuesSerializer(ModelSerializer):

    parent_lookup_kwargs = {
        'project_pk': 'project__pk',
    }

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'status', 'assignee_user', 'created_time']
        
    def create(self, validated_data):

        project_id = self.context['request'].parser_context['kwargs']['project_pk']

        validated_data['created_time'] = serializers.DateTimeField()
        validated_data['project'] = Project.objects.get(pk=project_id)
        print('coucou 1 : ', self.context.get("author_user"))

        if self.context.get("author_user") == None:
            print('coucou 2')
            validated_data['author_user'] = self.context['request'].user

        return super().create(validated_data)

class CommentsSerializer(ModelSerializer):
    
    parent_lookup_kwargs = {
        'project_pk': 'issue__project__pk',
        'issue_pk': 'issue__pk',
    }

    class Meta:
        model = Comments
        fields = ['id', 'description']

    def create(self, validated_data):
        issue_id = self.context['request'].parser_context['kwargs']['issue_pk']

        validated_data['issue'] = Issue.objects.get(pk=issue_id)
        validated_data['author_user'] = self.context['request'].user
        validated_data['created_time'] = serializers.DateTimeField()

        return super().create(validated_data)