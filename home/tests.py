from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Profile, Project
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from tempfile import TemporaryDirectory
from PIL import Image
from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError
import json
import environ
import os

env = environ.Env()
environ.Env.read_env()


class BaseTestWithTempMedia(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_media_dir = TemporaryDirectory() # Create a temporary directory
        cls.override = override_settings(MEDIA_ROOT=cls.temp_media_dir.name) # Override the MEDIA_ROOT setting
        cls.override.enable()

    @classmethod
    def tearDownClass(cls):
        cls.override.disable() # Disable the override
        cls.temp_media_dir.cleanup() # Cleanup the temporary directory
        super().tearDownClass()

# Main Page
class MainPageViewTests(BaseTestWithTempMedia):

    def setUp(self):
        img = Image.new('RGB', (100, 100), color='blue')
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        profile_image = SimpleUploadedFile("test_image.jpg", img_io.read(), content_type='image/jpeg')
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
        response = self.client.get(reverse('home/main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Get to know me!")

    def test_main_page_returns_name_from_database(self):
        #Walking skeleton
        response = self.client.get(reverse('home/main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testi mies")

    def test_main_page_introduction_displays(self):
        response = self.client.get(reverse('home/main_page'))
        self.assertContains(response, "Hello There")
        self.assertEqual(response.context['profile'].introduction, "Hello There")

    def test_main_page_uses_correct_template(self):
        response = self.client.get(reverse('home/main_page'))
        self.assertTemplateUsed(response, 'home/main_page.html')

    def test_main_page_displays_skills(self):
        response = self.client.get(reverse('home/main_page'))
        self.assertContains(response, "Juggling")
        self.assertContains(response, "handstands")
        self.assertContains(response, "coding")
        self.assertContains(response, "cooking")
        self.assertContains(response, "sleeping")
    
    def test_main_page_context_data(self):
        Profile.objects.all().delete()

        img = Image.new('RGB', (100, 100), color='blue')
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        profile_image = SimpleUploadedFile("test_image.jpg", img_io.read(), content_type='image/jpeg')

        profile = Profile.objects.create(name="Jane Doe", bio="Welcome to my portfolio.", email='jane@test.com', profile_image=profile_image)
        response = self.client.get(reverse('home/main_page'))
        self.assertEqual(response.context['profile'], profile)
    
    def test_main_page_displays_placeholder_when_no_profile(self):
        Profile.objects.all().delete()
        response = self.client.get(reverse('home/main_page'))
        self.assertContains(response, 'My Name')
 
# ProjectView NOT CURRENTLY IMPLEMENTED
""" 
class ProjectListViewTests(BaseTestWithTempMedia):

    def setUp(self):
        Project.objects.create(
            title = "Project1",
            description = "Nice project",
            short_description = "project",
            image = "",
            link = "www.testi.com",
            date_completed = "2025-01-13",
        )

    def test_projects_page_returns_200(self):
        response = self.client.get(reverse('home/projects'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Projects")
    
    def test_projects_page_correct_template(self):
        response = self.client.get(reverse('home/projects'))
        self.assertTemplateUsed(response, 'home/project_list.html')

    def test_projects_page_context_data(self):
        Project.objects.all().delete()

        project = Project.objects.create(
            title = "Context data Project",
            description = "Good project",
            short_description = "project",
            image = "",
            link = "www.contexttest.com",
            date_completed = "2024-01-10"
            )
        
        response = self.client.get(reverse('home/projects'))
        self.assertIn(project, response.context['projects'])
 """
#ProfileModel

class ProfileModelTests(BaseTestWithTempMedia):

    def setUp(self):
        img = Image.new('RGB', (100, 100), color='blue')
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        profile_image = SimpleUploadedFile("test_image.jpg", img_io.read(), content_type='image/jpeg')

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
        invalid_image = SimpleUploadedFile("test_image.txt", b"Invalid content", content_type="text/plain")
        profile = Profile(name="Test", email="test@test.com", profile_image=invalid_image)
        with self.assertRaises(ValidationError):
            profile.clean()

    def test_profile_name_max_length(self):
        max_length = Profile._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "Testi mies")

#ProjectModel

class ProjectModelTests(BaseTestWithTempMedia):

    def setUp(self):
        self.project = Project.objects.create(
            title = "Project1",
            description = "Nice project",
            image = "",
            link = "www.testi.com",
            date_completed = "2025-01-13",
        )

    def test_project_creation(self):
        self.assertEqual(self.project.title, "Project1")
        self.assertEqual(self.project.description, "Nice project")
        self.assertEqual(self.project.link, "www.testi.com")
        self.assertEqual(self.project.date_completed, "2025-01-13")

    def test_project_name_max_length(self):
        max_length = Project._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_project_str(self):
        self.assertEqual(str(self.project), "Project1")

#ContactForm

class ContactFormTests(BaseTestWithTempMedia):

    def test_contact_form_with_valid_data(self):
        data = {
            'name': 'Testi mies',
            'email': 'Testi@testi.fi',
            'message': 'Hello there!',
        }
        response = self.client.post(reverse('contact'), data)

        # Check for redirect after successful form submission
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['message'], "Thanks for contacting me!")
    
    def test_contact_form_with_invalid_data(self):
        data = {
            'name': '',
            'email': 'Testi@testi.fi',
            'message': 'Hello there!',
        }
        response = self.client.post(reverse('contact'), data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.', response.json()['errors']['name'])

    def test_contact_form_sends_email(self):
        data = {
            'name': 'Testi Mies',
            'email': 'Testi@testi.fi',
            'message': 'Hello there!',
        }
        response = self.client.post(reverse('contact'), data)

        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check email content and recipients
        email = mail.outbox[0]
        self.assertEqual(email.subject, "Contact Form Submission from Testi Mies")
        self.assertEqual(email.body, "Hello there!")
        self.assertEqual(email.from_email, 'Testi@testi.fi')

    def test_contact_form_email_error(self):
        data = {
            'name': '',
            'email': 'Testi@testi.fi',
            'message': 'Hello there!',
        }
        response = self.client.post(reverse('contact'), data)
        # Check if no email was sent (form is invalid)
        self.assertEqual(len(mail.outbox), 0)

    def test_empty_required_fields(self):
        data = {
            'name': '', 
            'email': 'testi@testi.fi',
            'message': 'Hello there!',
        }
        response = self.client.post(reverse('contact'), data)

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)

        self.assertIn('name', response_data['errors'])
        self.assertEqual(response_data['errors']['name'][0], 'This field is required.')

    def test_ajax_error_message(self):
        # Test the behavior of AJAX error messages (e.g., for invalid form submission)
        response = self.client.post(reverse('contact'), {'name': '', 'email': 'invalidemail', 'message': 'Hello'})
        
        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.content)
        # Check that the error for the 'name' field is present
        self.assertIn('name', response_data['errors'])
        self.assertEqual(response_data['errors']['name'][0], 'This field is required.')

        # Check if the error for the 'email' field is present
        self.assertIn('email', response_data['errors'])
        self.assertEqual(response_data['errors']['email'][0], 'Enter a valid email address.')


# Cloud storage tests
if os.getenv('RENDER') == 'true':
    class CloudStorageTests(BaseTestWithTempMedia):

        @override_settings(
            DEFAULT_FILE_STORAGE='storages.backends.s3boto3.S3botoStorage',
            AWS_ACCESS_KEY_ID = os.getenv('B2_APPLICATION_KEY_ID'),
            AWS_SECRET_ACCESS_KEY = os.getenv('B2_APPLICATION_KEY'),
            AWS_STORAGE_BUCKET_NAME = os.getenv('B2_TEST_BUCKET_NAME'),
        )

        def test_profile_upload_to_b2(self):
            img = Image.new('RGB', (100, 100), color='blue')
            img_io = BytesIO()
            img.save(img_io, 'JPEG')
            img_io.seek(0)
            profile_image = SimpleUploadedFile("test_image.jpg", img_io.read(), content_type='image/jpeg')

            profile = Profile.objects.create(
                name="Testi mies",
                bio="Hello World!",
                profile_image=profile_image,
            )

            s3 = boto3.client('s3')
            try:
                s3.head_object(Bucket=env('B2_TEST_BUCKET_NAME'), Key=f'media/profile_images/{profile.profile_image.name}')
                image_exists = True
            except NoCredentialsError:
                self.fail("B2 credentials not provided")
            except s3.exceptions.NoSuchKey:
                image_exists = False

            self.assertTrue(image_exists, "The image was not uploaded to B2")