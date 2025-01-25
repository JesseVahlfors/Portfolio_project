from django.test import TestCase, override_settings
from django.urls import reverse
from .models import Profile, Project
from django.core.files.uploadedfile import SimpleUploadedFile
from tempfile import TemporaryDirectory


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
        profile_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
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

        profile_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        profile = Profile.objects.create(name="Jane Doe", bio="Welcome to my portfolio.", email='jane@test.com', profile_image=profile_image)
        response = self.client.get(reverse('home/main_page'))
        self.assertEqual(response.context['profile'], profile)
    
    def test_main_page_displays_placeholder_when_no_profile(self):
        Profile.objects.all().delete()
        response = self.client.get(reverse('home/main_page'))
        self.assertContains(response, 'My Name')

        


class ProfileViewTests(BaseTestWithTempMedia):

    def setUp(self):
        profile_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        Profile.objects.all().delete()
        Profile.objects.create(
            name="Testi mies",
            bio="Hello World!",
            email="test@test.com",
            phone="555-1234567",
            profile_image=profile_image,
        )

    def test_profile_page_returns_200(self):
        response = self.client.get(reverse('home/profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About Me")

    def test_profile_page_correct_template(self):
        response = self.client.get(reverse('home/profile'))
        self.assertTemplateUsed(response, 'home/profile.html')

    def test_profile_page_context_data(self):
        Profile.objects.all().delete()

        profile_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        profile = Profile.objects.create(name="Jane Doe", bio="Welcome to my portfolio.", email='jane@test.com', profile_image=profile_image)
        response = self.client.get(reverse('home/profile'))
        self.assertEqual(response.context['profile'], profile)
    
    def test_profile_page_displays_placeholder_when_no_profile(self):
        Profile.objects.all().delete()
        response = self.client.get(reverse('home/profile'))
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
        profile_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

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