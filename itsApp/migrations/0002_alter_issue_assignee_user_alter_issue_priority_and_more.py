# Generated by Django 4.1.5 on 2023-01-24 05:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itsApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assignee_user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='issues_assignee_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.CharField(choices=[('faible', 'Faible'), ('moyen', 'Moyen'), ('elevée', 'Elevée')], max_length=6),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('a faire', 'A faire'), ('en cours', 'En cours'), ('termine', 'Terminé')], max_length=8),
        ),
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.CharField(choices=[('back-end', 'Back-end'), ('front-end', 'Front-end'), ('iOS', 'IOS'), ('android', 'Android')], max_length=15),
        ),
    ]
