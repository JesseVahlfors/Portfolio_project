# Generated by Django 5.1.4 on 2025-01-20 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_profile_introduction'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.TextField(null=True),
        ),
    ]
