from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank = True, null=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    introduction = models.TextField(null=True)
    skills = models.TextField(null=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    date_completed = models.DateField()

    def __str__(self):
        return self.title
