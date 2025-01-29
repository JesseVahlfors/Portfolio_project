from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError
import os
from django.utils.text import slugify
import bleach
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging
from io import BytesIO
logger = logging.getLogger("django")
logger.debug("This is a test debug message for file uploads.")

class Profile(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank = True, null=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    introduction = models.TextField(null=True)
    about_me_intro = models.TextField(null=True)
    skills = models.TextField(null=True)
    linkedin = models.URLField(null=True)
    github = models.URLField(null=True)

    def clean_html(self, value):
        allowed_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'strong', 'em', 'u', 's', 'a', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'img']
        return bleach.clean(value, tags=allowed_tags)
    
    def clean(self):
        # Custom validation for image type
        if self.profile_image:
            try:
                # Check if the uploaded file is an image
                img = Image.open(self.profile_image)
                img.verify()  # Verifies if the file is a valid image
            except (IOError, SyntaxError):
                raise ValidationError("Invalid image file.")

    def save(self, *args, **kwargs):
        logger.debug(f"Uploading file: {self.profile_image.name} using {default_storage}")
        file_url = default_storage.url(self.profile_image.name)
        logger.debug(f"File uploaded to: {file_url}")
        
        if self.bio:
            self.bio = self.clean_html(self.bio)

        if self.pk and self.profile_image:
            old_profile = Profile.objects.get(pk=self.pk)
            if old_profile.profile_image and old_profile.profile_image != self.profile_image:
                if default_storage.exists(old_profile.profile_image.name):
                    default_storage.delete(old_profile.profile_image.name)  # Delete old image from cloud storage

        if default_storage.exists(self.profile_image.name):
            logger.debug("File already exists in storage!")
            

        super(Profile, self).save(*args, **kwargs)

        if self.profile_image:
            try:
                with default_storage.open(self.profile_image.name, 'rb') as f:
                    img = Image.open(f)
                    img.thumbnail((240, 240))

                    # Save the resized image in memory
                    buffer = BytesIO()
                    img.save(buffer, format='JPEG')

                    # Overwrite the existing image in storage
                    default_storage.save(self.profile_image.name, ContentFile(buffer.getvalue()))

            except (UnidentifiedImageError, OSError) as e:
                # Handle the exception, log it, or ignore it during tests
                logger.error(f"Error resizing image: {e}")
                print(f"Error resizing image: {e}")
        
        logger.debug(f"File uploaded to: {self.profile_image.url}")

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
