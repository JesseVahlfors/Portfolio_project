import logging
from io import BytesIO

import bleach
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger("django")
logger.debug("This is a test debug message for file uploads.")


class Profile(models.Model):
    # Basic information
    name = models.CharField(max_length=100)

    profile_image = models.ImageField(
        upload_to="profile_images",
        blank=True,
        null=True,
        help_text="Profile image displayed on the portfolio site.",
    )

    # Homepage content
    bio = models.TextField(help_text="Short bio displayed on the portfolio home page.")

    introduction = models.TextField(
        blank=True,
        null=True,
        help_text="Short intro shown at the start of the About Me section.",
    )

    # About page content
    about_me_intro = models.TextField(
        blank=True, null=True, help_text="Extended introduction for the About Me page."
    )

    skills = models.TextField(
        blank=True, null=True, help_text="List of skills or technologies."
    )

    # Contact information
    email = models.EmailField()

    phone = models.CharField(
        max_length=15, blank=True, null=True, help_text="Contact phone number."
    )

    # External profiles
    linkedin = models.URLField(
        blank=True, null=True, help_text="Link to LinkedIn profile."
    )

    github = models.URLField(blank=True, null=True, help_text="Link to GitHub profile.")

    def clean_html(self, value):
        allowed_tags = [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "strong",
            "em",
            "u",
            "s",
            "a",
            "ul",
            "ol",
            "li",
            "blockquote",
            "code",
            "pre",
            "img",
        ]
        return bleach.clean(value, tags=allowed_tags)

    def clean(self):
        # Custom validation for image type
        if self.profile_image:
            try:
                # Check if the uploaded file is an image
                img = Image.open(self.profile_image)
                img.verify()  # Verifies if the file is a valid image
            except (OSError, SyntaxError):
                raise ValidationError("Invalid image file.")

    def save(self, *args, **kwargs):

        # Clean the HTML content
        if self.bio:
            self.bio = self.clean_html(self.bio)

        # Delete the old image file if a new one is uploaded
        if self.pk and self.profile_image:
            old_profile = Profile.objects.get(pk=self.pk)
            if (
                old_profile.profile_image
                and old_profile.profile_image != self.profile_image
            ) and old_profile.profile_image.storage.exists(
                old_profile.profile_image.name
            ):
                old_profile.profile_image.storage.delete(old_profile.profile_image.name)

        # Save the model instance
        super().save(*args, **kwargs)

        # Resize the image
        if self.profile_image:
            try:
                with self.profile_image.storage.open(
                    self.profile_image.name, "rb"
                ) as f:
                    img = Image.open(f)
                    img.thumbnail((240, 240))

                    # Save the resized image in memory
                    buffer = BytesIO()
                    img_format = img.format if img.format else "JPEG"
                    img.save(buffer, format=img_format)

                    # Overwrite the existing image in storage
                    self.profile_image.storage.save(
                        self.profile_image.name, ContentFile(buffer.getvalue())
                    )

            except (UnidentifiedImageError, OSError) as e:
                # Handle the exception, log it, or ignore it during tests
                logger.error(f"Error resizing image: {e}")

    def __str__(self):
        return self.name


class Project(models.Model):
    # Basic project information
    title = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        max_length=200,
        blank=True,
        null=True,
        help_text="URL slug for the project's detail page (auto-generated if left empty).",
    )

    date_completed = models.DateField()

    is_featured = models.BooleanField(
        default=False,
        help_text="Display this project in the featured projects section.",
    )

    # Project card / listing
    list_summary = models.TextField(
        blank=True, null=True, help_text="Short blurb shown in the project list/grid."
    )

    image = models.ImageField(
        upload_to="project_images",
        blank=True,
        null=True,
        help_text="Optional thumbnail image for the project page or project list.",
    )

    # Project detail page
    hero_text = models.TextField(
        blank=True,
        null=True,
        help_text="Hero section intro shown at the top of the project detail page.",
    )

    detail_description = models.TextField(
        help_text="Full HTML description for the project detail page.",
        blank=True,
        null=True,
    )

    skills = models.TextField(
        blank=True, null=True, help_text="Skills or technologies used in this project."
    )

    # External links
    link = models.URLField(
        blank=True,
        null=True,
        help_text="URL to the live website or interactive demo for this project.",
    )

    project_github = models.URLField(
        blank=True,
        null=True,
        help_text="Link to the GitHub repository for this project.",
    )

    pypi_url = models.URLField(
        blank=True,
        null=True,
        help_text="Link to the project's PyPI package (if applicable).",
    )

    def get_absolute_url(self):
        return reverse("home/project_detail", args=[self.slug])

    def clean_html(self, value):
        allowed_tags = [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "strong",
            "em",
            "u",
            "s",
            "a",
            "ul",
            "ol",
            "li",
            "blockquote",
            "code",
            "pre",
            "img",
            "hr",
        ]
        return bleach.clean(value, tags=allowed_tags)

    def save(self, *args, **kwargs):
        if self.detail_description:
            self.detail_description = self.clean_html(self.detail_description)

        if not self.slug:
            base_slug = slugify(self.title) or "project"
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
