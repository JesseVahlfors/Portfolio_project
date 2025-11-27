from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.core.files.base import ContentFile
from PIL import Image, UnidentifiedImageError
import os
import bleach
import logging
from io import BytesIO
logger = logging.getLogger("django")
logger.debug("This is a test debug message for file uploads.")

class Profile(models.Model):
    name = models.CharField(max_length=100)

    bio = models.TextField(
        help_text="Short bio displayed on the portfolio home page."
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Contact phone number."
    )

    profile_image = models.ImageField(
        upload_to='profile_images',
        blank=True,
        null=True,
        help_text="Profile image displayed on the portfolio site."
    )

    introduction = models.TextField(
        blank=True,
        null=True,
        help_text="Short intro shown at the start of the About Me section."
    )

    about_me_intro = models.TextField(
        blank=True,
        null=True,
        help_text="Extended introduction for the About Me page."
    )

    skills = models.TextField(
        blank=True,
        null=True,
        help_text="List of skills or technologies."
    )

    linkedin = models.URLField(
        blank=True,
        null=True,
        help_text="Link to LinkedIn profile."
    )

    github = models.URLField(
        blank=True,
        null=True,
        help_text="Link to GitHub profile."
    )

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
        
        # Clean the HTML content
        if self.bio:
            self.bio = self.clean_html(self.bio)

        # Delete the old image file if a new one is uploaded
        if self.pk and self.profile_image:  
            old_profile = Profile.objects.get(pk=self.pk)
            if old_profile.profile_image and old_profile.profile_image != self.profile_image:
                if old_profile.profile_image.storage.exists(old_profile.profile_image.name):
                    old_profile.profile_image.storage.delete(old_profile.profile_image.name) 

        # Save the model instance    
        super(Profile, self).save(*args, **kwargs)

        # Resize the image
        if self.profile_image:
            try:
                with self.profile_image.storage.open(self.profile_image.name, 'rb') as f:
                    img = Image.open(f)
                    img.thumbnail((240, 240))

                    # Save the resized image in memory
                    buffer = BytesIO()
                    img_format = img.format if img.format else 'JPEG'
                    img.save(buffer, format=img_format)

                    # Overwrite the existing image in storage
                    self.profile_image.storage.save(self.profile_image.name, ContentFile(buffer.getvalue()))

            except (UnidentifiedImageError, OSError) as e:
                # Handle the exception, log it, or ignore it during tests
                logger.error(f"Error resizing image: {e}")
        

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)

    list_summary = models.TextField(
        blank=True,
        null=True,
        help_text="Short blurb shown in the project list/grid."
    )

    hero_text = models.TextField(
        blank=True,
        null=True,
        help_text="Hero section intro shown at the top of the project detail page."
    )

    detail_description = models.TextField(
        help_text="Full HTML description for the project detail page.",
        blank=True,
        null=True,
    )

    image = models.ImageField(
        upload_to='project_images',
        blank=True,
        null=True,
        help_text="Optional thumbnail image for the project page or project list."
    )

    link = models.URLField(
        blank=True,
        null=True,
        help_text="URL to the live website or interactive demo for this project."
    )

    date_completed = models.DateField()

    slug = models.SlugField(
        unique=True,
        max_length=200,
        blank=True,
        null=True,
        help_text="URL slug for the project's detail page (auto-generated if left empty)."
    )

    skills = models.TextField(
        blank=True,
        null=True,
        help_text="Skills or technologies used in this project."
    )

    project_github = models.URLField(
        blank=True,
        null=True,
        help_text="Link to the GitHub repository for this project."
    )

    pypi_url = models.URLField(
        blank=True,
        null=True,
        help_text="Link to the project's PyPI package (if applicable)."
    )


    def get_absolute_url(self):
        return reverse('home/project_detail', args=[str(self.id)])

    def clean_html(self, value):
        allowed_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'strong', 'em', 'u', 's', 'a', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'img']
        return bleach.clean(value, tags=allowed_tags)

    def save(self, *args, **kwargs):
        if self.detail_description:
            self.detail_description = self.clean_html(self.detail_description)

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
