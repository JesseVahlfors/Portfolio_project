from django.test import TestCase, override_settings
from django.urls import reverse
from .models import Profile, Project
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from tempfile import TemporaryDirectory
from PIL import Image
from io import BytesIO


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

    def test_profile_name_max_length(self):
        max_length = Profile._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "Testi mies")

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


class ContactFormTests(BaseTestWithTempMedia):

    def test_contact_form_with_valid_data(self):
        data = {
            'name': 'Testi mies',
            'email': 'Testi@testi.fi',
            'message': 'Hello there!',
        }
        response = self.client.post(reverse('contact'), data)

        # Check for redirect after successful form submission
        self.assertRedirects(response, '/#contact')

        storage = get_messages(response.wsgi_request)
        message = list(storage)[0]
        self.assertEqual(str(message), "Your message has been successfully sent. I'll get back to you soon!")
    
    def test_contact_form_with_invalid_data(self):
        data = {
            'name': '',
            'email': 'Testi@testi.fi',
            'message': 'Hello there!',
        }
        response = self.client.post(reverse('contact'), data)

        self.assertFormError(response, 'form', 'name', 'This field is required.')



    # 2. Test the contact form with valid data
    # Test submitting the contact form with valid data and ensure it is processed correctly (e.g., redirects to success page).

    # 3. Test the contact form with invalid data
    # Test submitting the contact form with invalid or missing data and ensure appropriate validation errors are displayed.

    # 4. Test the contact form redirects after successful submission
    # Test that after submitting the form with valid data, the user is redirected to a success page.

    # 5. Test if an email is sent on form submission (if applicable)
    # Test that when the form is submitted successfully, an email is sent (for example, to the admin email).

    # 6. Test empty fields (Required field validation)
    # Test that when the form is submitted with empty required fields, validation errors are shown.
