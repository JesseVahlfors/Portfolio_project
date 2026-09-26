import os
import unittest
from io import BytesIO
from tempfile import TemporaryDirectory
from unittest.mock import patch

import boto3
import environ
from botocore.exceptions import NoCredentialsError
from django.core import mail
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Profile, Project

env = environ.Env()
environ.Env.read_env()

env = environ.Env()
environ.Env.read_env()


class BaseTestWithTempMedia(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_media_dir = TemporaryDirectory()  # Create a temporary directory
        cls.override = override_settings(
            MEDIA_ROOT=cls.temp_media_dir.name
        )  # Override the MEDIA_ROOT setting
        cls.override.enable()

    @classmethod
    def tearDownClass(cls):
        cls.override.disable()  # Disable the override
        cls.temp_media_dir.cleanup()  # Cleanup the temporary directory
        super().tearDownClass()


# Main Page
class MainPageViewTests(BaseTestWithTempMedia):
    def setUp(self):
        img = Image.new("RGB", (100, 100), color="blue")
        img_io = BytesIO()
        img.save(img_io, "JPEG")
        img_io.seek(0)
        profile_image = SimpleUploadedFile(
            "test_image.jpg", img_io.read(), content_type="image/jpeg"
        )
        Profile.objects.all().delete()
        Profile.objects.create(
            name="Testi mies",
            bio="Hello World!",
            email="test@test.com",
            introduction="Hello There",
            profile_image=profile_image,
            skills="Juggling, handstands, coding, cooking, sleeping",
        )

    def test_main_page_returns_200(self):
        response = self.client.get(reverse("home/main_page"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Get to know me!")

    def test_main_page_returns_name_from_database(self):
        # Walking skeleton
        response = self.client.get(reverse("home/main_page"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testi mies")

    def test_main_page_introduction_displays(self):
        response = self.client.get(reverse("home/main_page"))
        self.assertContains(response, "Hello There")
        self.assertEqual(response.context["profile"].introduction, "Hello There")

    def test_main_page_uses_correct_template(self):
        response = self.client.get(reverse("home/main_page"))
        self.assertTemplateUsed(response, "home/main_page.html")

    def test_main_page_displays_skills(self):
        response = self.client.get(reverse("home/main_page"))
        self.assertContains(response, "Juggling")
        self.assertContains(response, "handstands")
        self.assertContains(response, "coding")
        self.assertContains(response, "cooking")
        self.assertContains(response, "sleeping")

    def test_main_page_context_data(self):
        Profile.objects.all().delete()

        img = Image.new("RGB", (100, 100), color="blue")
        img_io = BytesIO()
        img.save(img_io, "JPEG")
        img_io.seek(0)
        profile_image = SimpleUploadedFile(
            "test_image.jpg", img_io.read(), content_type="image/jpeg"
        )

        profile = Profile.objects.create(
            name="Jane Doe",
            bio="Welcome to my portfolio.",
            email="jane@test.com",
            profile_image=profile_image,
        )
        response = self.client.get(reverse("home/main_page"))
        self.assertEqual(response.context["profile"], profile)

    def test_main_page_displays_placeholder_when_no_profile(self):
        Profile.objects.all().delete()
        response = self.client.get(reverse("home/main_page"))
        self.assertContains(response, "My Name")


# Project View Tests
class ProjectViewTests(BaseTestWithTempMedia):
    def setUp(self):
        self.featured_old = Project.objects.create(
            title="Featured Old",
            date_completed="2025-01-01",
            is_featured=True,
        )
        self.featured_new = Project.objects.create(
            title="Featured New",
            date_completed="2025-03-01",
            is_featured=True,
        )
        self.unfeatured = Project.objects.create(
            title="Unfeatured Project",
            date_completed="2025-04-01",
            is_featured=False,
        )

    def test_main_page_only_contains_featured_projects(self):
        response = self.client.get(reverse("home/main_page"))

        projects = list(response.context["projects"])

        self.assertIn(self.featured_old, projects)
        self.assertIn(self.featured_new, projects)
        self.assertNotIn(self.unfeatured, projects)

    def test_main_page_limits_featured_projects_to_three(self):
        Project.objects.create(
            title="Featured Three",
            date_completed="2025-02-01",
            is_featured=True,
        )
        Project.objects.create(
            title="Featured Four",
            date_completed="2024-12-01",
            is_featured=True,
        )

        response = self.client.get(reverse("home/main_page"))

        self.assertEqual(len(response.context["projects"]), 3)

    def test_main_page_orders_featured_projects_newest_first(self):
        response = self.client.get(reverse("home/main_page"))

        projects = list(response.context["projects"])

        self.assertEqual(projects, [self.featured_new, self.featured_old])

    def test_projects_page_returns_200(self):
        response = self.client.get(reverse("home/projects"))

        self.assertEqual(response.status_code, 200)

    def test_projects_page_uses_correct_template(self):
        response = self.client.get(reverse("home/projects"))

        self.assertTemplateUsed(response, "home/project_list.html")

    def test_projects_page_contains_featured_and_unfeatured_projects(self):
        response = self.client.get(reverse("home/projects"))

        projects = list(response.context["projects"])

        self.assertIn(self.featured_old, projects)
        self.assertIn(self.featured_new, projects)
        self.assertIn(self.unfeatured, projects)

    def test_projects_page_orders_projects_newest_first(self):
        response = self.client.get(reverse("home/projects"))

        projects = list(response.context["projects"])

        self.assertEqual(
            projects,
            [self.unfeatured, self.featured_new, self.featured_old],
        )

    def test_projects_with_same_date_use_newest_created_first(self):
        first = Project.objects.create(
            title="First",
            date_completed="2025-05-01",
        )
        second = Project.objects.create(
            title="Second",
            date_completed="2025-05-01",
        )

        response = self.client.get(reverse("home/projects"))
        projects = list(response.context["projects"])

        self.assertLess(projects.index(second), projects.index(first))


# ProfileModel


class ProfileModelTests(BaseTestWithTempMedia):
    def setUp(self):
        img = Image.new("RGB", (100, 100), color="blue")
        img_io = BytesIO()
        img.save(img_io, "JPEG")
        img_io.seek(0)
        profile_image = SimpleUploadedFile(
            "test_image.jpg", img_io.read(), content_type="image/jpeg"
        )

        self.profile = Profile.objects.create(
            name="Testi mies",
            bio="Hello World!",
            email="test@test.com",
            phone="555-1234567",
            profile_image=profile_image,
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.name, "Testi mies")
        self.assertEqual(self.profile.bio, "Hello World!")
        self.assertEqual(self.profile.email, "test@test.com")
        self.assertEqual(self.profile.phone, "555-1234567")

    def test_profile_creation_with_profile_image(self):
        self.assertTrue(self.profile.profile_image)

    def test_profile_invalid_image_upload(self):
        invalid_image = SimpleUploadedFile(
            "test_image.txt", b"Invalid content", content_type="text/plain"
        )
        profile = Profile(
            name="Test", email="test@test.com", profile_image=invalid_image
        )
        with self.assertRaises(ValidationError):
            profile.clean()

    def test_profile_name_max_length(self):
        max_length = Profile._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "Testi mies")


# ProjectModel


class ProjectModelTests(BaseTestWithTempMedia):
    def setUp(self):
        self.project = Project.objects.create(
            title="Project1",
            detail_description="Nice project",
            image="",
            link="www.testi.com",
            date_completed="2025-01-13",
        )

    def test_project_creation(self):
        self.assertEqual(self.project.title, "Project1")
        self.assertEqual(self.project.detail_description, "Nice project")
        self.assertEqual(self.project.link, "www.testi.com")
        self.assertEqual(self.project.date_completed, "2025-01-13")

    def test_project_name_max_length(self):
        max_length = Project._meta.get_field("title").max_length
        self.assertEqual(max_length, 200)

    def test_project_str(self):
        self.assertEqual(str(self.project), "Project1")

    def test_project_get_absolute_url_uses_slug(self):
        self.assertEqual(
            self.project.get_absolute_url(),
            f"/projects/{self.project.slug}/",
        )

    def test_titles_without_slug_characters_have_working_card_links(self):
        Project.objects.create(title="Project", date_completed="2025-01-01")
        projects = []
        for title, expected_slug in [("!!!", "project-1"), ("你好", "project-2")]:
            with self.subTest(title=title):
                project = Project.objects.create(
                    title=title,
                    date_completed="2025-01-01",
                    is_featured=True,
                )
                project.refresh_from_db()
                self.assertEqual(project.slug, expected_slug)
                project.save()
                project.refresh_from_db()
                self.assertEqual(project.slug, expected_slug)
                detail_response = self.client.get(project.get_absolute_url())
                self.assertEqual(detail_response.status_code, 200)
                self.assertEqual(detail_response.context["project"], project)
                projects.append(project)

        for route in ["home/main_page", "home/projects"]:
            with self.subTest(route=route):
                response = self.client.get(reverse(route))
                self.assertEqual(response.status_code, 200)
                for project in projects:
                    self.assertContains(
                        response, f'href="{project.get_absolute_url()}"'
                    )


# ContactForm


class ContactFormTests(BaseTestWithTempMedia):
    @override_settings(
        DEFAULT_FROM_EMAIL="portfolio@test.com",
        CONTACT_TO_EMAIL="owner@test.com",
    )
    @patch("home.views.requests.post")
    def test_contact_form_with_valid_data(self, mock_post):
        mock_post.return_value.json.return_value = {"success": True}

        data = {
            "name": "Testi Mies",
            "email": "testi@testi.fi",
            "message": "Hello there!",
            "g-recaptcha-response": "valid-token",
        }

        response = self.client.post(reverse("contact"), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/partials/contact_form.html")
        self.assertTrue(response.context["success"])

    @patch("home.views.requests.post")
    def test_contact_form_with_invalid_data(self, mock_post):
        mock_post.return_value.json.return_value = {"success": True}

        data = {
            "name": "",
            "email": "testi@testi.fi",
            "message": "Hello there!",
            "g-recaptcha-response": "valid-token",
        }

        response = self.client.post(reverse("contact"), data)

        self.assertEqual(response.status_code, 400)
        self.assertFormError(
            response.context["form"], "name", "This field is required."
        )

    @override_settings(
        DEFAULT_FROM_EMAIL="portfolio@test.com",
        CONTACT_TO_EMAIL="owner@test.com",
    )
    @patch("home.views.requests.post")
    def test_contact_form_sends_email(self, mock_post):
        mock_post.return_value.json.return_value = {"success": True}

        data = {
            "name": "Testi Mies",
            "email": "testi@testi.fi",
            "message": "Hello there!",
            "g-recaptcha-response": "valid-token",
        }

        self.client.post(reverse("contact"), data)

        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]

        self.assertEqual(
            email.subject,
            "Contact Form Submission from Testi Mies",
        )
        self.assertEqual(
            email.body,
            "Name: Testi Mies\nEmail: testi@testi.fi\n\nMessage:\nHello there!",
        )
        self.assertEqual(email.from_email, "portfolio@test.com")
        self.assertEqual(email.to, ["owner@test.com"])
        self.assertEqual(email.reply_to, ["testi@testi.fi"])

    def test_contact_form_requires_recaptcha(self):
        data = {
            "name": "Testi Mies",
            "email": "testi@testi.fi",
            "message": "Hello there!",
        }

        response = self.client.post(reverse("contact"), data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.context["recaptcha_error"],
            "Please complete the reCAPTCHA.",
        )

    @patch("home.views.requests.post")
    def test_contact_form_rejects_failed_recaptcha(self, mock_post):
        mock_post.return_value.json.return_value = {"success": False}

        data = {
            "name": "Testi Mies",
            "email": "testi@testi.fi",
            "message": "Hello there!",
            "g-recaptcha-response": "invalid-token",
        }

        response = self.client.post(reverse("contact"), data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.context["recaptcha_error"],
            "reCAPTCHA verification failed. Please try again.",
        )


# Cloud storage tests
@unittest.skipIf(
    "storages.backends.s3boto3" not in str(os.getenv("DEFAULT_FILE_STORAGE", "")),
    "S3 storage not configured",
)
class CloudStorageTests(BaseTestWithTempMedia):
    @override_settings(
        DEFAULT_FILE_STORAGE="storages.backends.s3boto3.S3Boto3Storage",
        AWS_ACCESS_KEY_ID=os.getenv("B2_APPLICATION_KEY_ID"),
        AWS_SECRET_ACCESS_KEY=os.getenv("B2_APPLICATION_KEY"),
        AWS_STORAGE_BUCKET_NAME=os.getenv("B2_BUCKET_NAME"),
        AWS_REQUEST_CHECKSUM_CALCULATION=os.getenv(
            "AWS_REQUEST_CHECKSUM_CALCULATION", "WHEN_REQUIRED"
        ),
        AWS_RESPONSE_CHECKSUM_VALIDATION=os.getenv(
            "AWS_RESPONSE_CHECKSUM_VALIDATION", "WHEN_REQUIRED"
        ),
        AWS_S3_ENDPOINT_URL=f"https://s3.{os.getenv('B2_REGION_NAME', 'us-west-002')}.backblazeb2.com",
    )
    def setUp(self):
        super().setUp()
        self.boto3_session = boto3.Session(
            aws_access_key_id=os.getenv("B2_APPLICATION_KEY_ID"),
            aws_secret_access_key=os.getenv("B2_APPLICATION_KEY"),
        )
        self.boto3_session._session.set_config_variable(
            "s3",
            {
                "checksum_calculation": os.getenv(
                    "AWS_REQUEST_CHECKSUM_CALCULATION", "WHEN_REQUIRED"
                ),
                "checksum_validation": os.getenv(
                    "AWS_RESPONSE_CHECKSUM_VALIDATION", "WHEN_REQUIRED"
                ),
            },
        )
        self.s3 = self.boto3_session.client(
            "s3", endpoint_url="https://s3.eu-central-003.backblazeb2.com"
        )
        self.bucket_name = os.getenv("B2_BUCKET_NAME")

    def test_profile_upload_to_b2(self):
        img = Image.new("RGB", (100, 100), color="blue")
        img_io = BytesIO()
        img.save(img_io, "JPEG")
        img_io.seek(0)
        profile_image = SimpleUploadedFile(
            "test_image.jpg", img_io.read(), content_type="image/jpeg"
        )

        profile = Profile.objects.create(
            name="Testi mies",
            bio="Hello World!",
            profile_image=profile_image,
        )

        try:
            self.s3.head_object(
                Bucket=self.bucket_name, Key=f"{profile.profile_image.name}"
            )
            image_exists = True
        except NoCredentialsError:
            self.fail("B2 credentials not provided")
        except self.s3.exceptions.NoSuchKey:
            image_exists = False

        self.assertTrue(image_exists, "The image was not uploaded to B2")

    def tearDown(self):
        try:
            self.s3.delete_object(
                Bucket=self.bucket_name, Key="profile_images/test_image.jpg"
            )
        except self.s3.exceptions.NoSuchKey:
            pass
        super().tearDown()
