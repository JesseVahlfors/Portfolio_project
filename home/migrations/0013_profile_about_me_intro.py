# Generated by Django 5.1.4 on 2025-01-27 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_project_project_github'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about_me_intro',
            field=models.TextField(null=True),
        ),
    ]
