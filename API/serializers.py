from rest_framework.serializers import ModelSerializer,\
    HyperlinkedModelSerializer
from rest_framework import serializers
from .models import Project, Contributor, Issue, Comments
from authentication.models import User


class ProjectSerializer(HyperlinkedModelSerializer):
    author_user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']

    def create(self, validated_data):
        validated_data['author_user_id'] = self.context['request'].user.id
        return super().create(validated_data)


class ContributorSerializer(ModelSerializer):

    project = serializers.PrimaryKeyRelatedField(read_only=True)
    # user = UserSerializer(required=False)

    parent_lookup_kwargs = {
        'project_pk': 'project__pk',
    }

    class Meta:
        model = Contributor
        fields = ['id', 'project', 'user', 'permission', 'role']

    def create(self, validated_data):
        project_id = self.context['request'].\
            parser_context['kwargs']['project_pk']
        validated_data['project'] = Project.objects.get(pk=project_id)
        return super().create(validated_data)


class IssuesSerializer(ModelSerializer):

    parent_lookup_kwargs = {
        'project_pk': 'project__pk',
    }

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'project_id', 'tag',
                  'priority', 'assignee_user', 'status', 'created_time']

    def create(self, validated_data):
        project_id = self.context['view'].kwargs['project_pk']
        project = Project.objects.get(pk=project_id)
        request = self.context['request']
        user = request.user

        validated_data['created_time'] = serializers.DateTimeField()
        validated_data['project'] = project
        validated_data['author_user'] = user

        assignee_user_id = validated_data.pop('assignee_user_id', None)

        if assignee_user_id:
            assignee_user = User.objects.get(pk=assignee_user_id)
            validated_data['assignee_user'] = assignee_user
        else:
            validated_data['assignee_user'] = user

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
