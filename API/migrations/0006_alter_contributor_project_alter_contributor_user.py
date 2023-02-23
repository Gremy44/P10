# Generated by Django 4.1.5 on 2023-02-14 05:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_alter_contributor_project_alter_contributor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributor_project', to='API.project'),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributor_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
