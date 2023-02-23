from django.db import models
from django.conf import settings

class Contributor(models.Model):

    PERMISSION = (
        ('authorized', 'Authorized'),
        ('unauthorized', 'Unauthorized'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributor_user')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='contributor_project')
    permission = models.CharField(max_length=15, choices=PERMISSION)
    role = models.CharField(max_length=50)


class Project(models.Model):

    TYPE = (
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'IOS'),
        ('android', 'Android'),
    )

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=15, choices=TYPE)
    author_user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Issue(models.Model):

    PRIORITY = (
        ('faible', 'Faible'),
        ('moyen', 'Moyen'),
        ('elevee', 'Elevée'),
    )

    TAG = (
        ('bug', 'Bug'),
        ('amelioration', 'Amélioration'),
        ('tache', 'Tache'),
    )

    STATUS = (
        ('a faire', 'A faire'),
        ('en cours', 'En cours'),
        ('termine', 'Terminé'),
    )

    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    tag = models.CharField(max_length=50)
    priority = models.CharField(max_length=6, choices=PRIORITY)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS)
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issues_author_user')
    assignee_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, related_name='issues_assignee_user')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    description = models.CharField(max_length=500)
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey('Issue', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description