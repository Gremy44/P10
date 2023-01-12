from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Contributor(models.Model):

    PERMISSION = (
        ('ok', 'Ok'),
        ('pas ok', 'Pas Ok'),
    )

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=PERMISSION)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.user

class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=50)
    author_user= models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Issue(models.Model):
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    tag = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    author_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='issues_author_user')
    assignee_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='issues_assignee_user')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comments(models.Model):
    description = models.CharField(max_length=500)
    author_user = models.ForeignKey('User', on_delete=models.CASCADE)
    issue = models.ForeignKey('Issue', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description