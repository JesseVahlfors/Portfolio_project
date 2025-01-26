from django.db import models
from PIL import Image
import os
from django.utils.text import slugify
import bleach

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

    def clean_html(self, value):
        allowed_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'strong', 'em', 'u', 's', 'a', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'img']
        return bleach.clean(value, tags=allowed_tags)
    

    def save(self, *args, **kwargs):
        if self.bio:
            self.bio = self.clean_html(self.bio)

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
    slug = models.SlugField(unique=True, null=True, max_length=200)
    skills = models.TextField(null=True)
    project_github = models.URLField(null=True)

    def clean_html(self, value):
        allowed_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'strong', 'em', 'u', 's', 'a', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'img']
        return bleach.clean(value, tags=allowed_tags)

    def save(self, *args, **kwargs):
        if self.description:
            self.description = self.clean_html(self.description)
            
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
