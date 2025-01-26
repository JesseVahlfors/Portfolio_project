from django.db import models
from PIL import Image
import os

class Profile(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank = True, null=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    introduction = models.TextField(null=True)
    skills = models.TextField(null=True)
    linkedin = models.URLField(null=True)
    github = models.URLField(null=True)

    def save(self, *args, **kwargs):
        if self.profile_image:
            if self.pk:
                old_profile = Profile.objects.get(pk=self.pk)
                if old_profile.profile_image and old_profile.profile_image != self.profile_image:
                    if os.path.isfile(old_profile.profile_image.path):
                        os.remove(old_profile.profile_image.path)

        super(Profile, self).save(*args, **kwargs)

        if self.profile_image:
            if self.profile_image.path:
                img = Image.open(self.profile_image.path)
                img.thumbnail((240, 240))
                img.save(self.profile_image.path)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.TextField(null=True)
    image = models.ImageField(upload_to='project_images', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    date_completed = models.DateField()

    def __str__(self):
        return self.title
