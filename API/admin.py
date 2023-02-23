from django.contrib import admin
from API.models import Contributor, Issue, Project, Comments


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'author_user', 'type')
    list_filter = ('id', 'title', 'author_user', 'type')

# admin.site.register(Project, ProjectAdmin)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'permission', 'role', 'project', 'user')
    list_filter = ('id', 'permission', 'role', 'project', 'user')

# admin.site.register(Contributor, ContributorAdmin)

class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'desc', 'tag', 'priority', 'created_time', 'assignee_user', 'author_user', 'project', 'status')
    list_filter = ('id', 'title', 'tag', 'priority', 'created_time', 'assignee_user', 'author_user', 'project', 'status')

# admin.site.register(Issue, IssueAdmin)

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'created_time', 'author_user', 'issue')
    list_filter = ('id', 'created_time', 'author_user', 'issue')

# admin.site.register(Comments, CommentsAdmin)

order = [Project, Contributor, Issue, Comments]

for model in order:
    admin.site.register(model, locals()[model.__name__+'Admin'])