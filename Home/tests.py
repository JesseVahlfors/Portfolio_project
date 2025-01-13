from django.test import TestCase
from django.urls import reverse
from .models import Profile, Project

class MainPageViewTests(TestCase):

    def setUp(self):
        Profile.objects.create(
            name="Testi mies",
            bio="Hello World!",
            email="test@test.com",
        )

    def test_main_page_returns_200(self):
        response = self.client.get(reverse('home/main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to My Portfolio")

    def test_main_page_returns_name_from_database(self):
        #Walking skeleton
        response = self.client.get(reverse('home/main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testi mies")

    def test_main_page_uses_correct_template(self):
        response = self.client.get(reverse('home/main_page'))
        self.assertTemplateUsed(response, 'home/main_page.html')

    def test_main_page_context_data(self):
        Profile.objects.all().delete()

        profile = Profile.objects.create(name="Jane Doe", bio="Welcome to my portfolio.", email='jane@test.com')
        response = self.client.get(reverse('home/main_page'))
        self.assertEqual(response.context['profile'], profile)
    
    def test_main_page_displays_placeholder_when_no_profile(self):
        Profile.objects.all().delete()
        response = self.client.get(reverse('home/main_page'))
        self.assertContains(response, 'My Name')


class ProfileViewTests(TestCase):

    def setUp(self):
        Profile.objects.create(
            name="Testi mies",
            bio="Hello World!",
            email="test@test.com",
            phone="555-1234567",
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

        profile = Profile.objects.create(name="Jane Doe", bio="Welcome to my portfolio.", email='jane@test.com')
        response = self.client.get(reverse('home/profile'))
        self.assertEqual(response.context['profile'], profile)
    
    def test_profile_page_displays_placeholder_when_no_profile(self):
        Profile.objects.all().delete()
        response = self.client.get(reverse('home/profile'))
        self.assertContains(response, 'My Name')

class ProjectListViewTests(TestCase):

    def setUp(self):
        Project.objects.create(
            title = "Project1",
            description = "Nice project",
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
            image = "",
            link = "www.contexttest.com",
            date_completed = "2024-01-10"
            )
        
        response = self.client.get(reverse('home/projects'))
        self.assertIn(project, response.context['projects'])


class ProfileModelTests(TestCase):

    def setUp(self):
        self.profile = Profile.objects.create(
            name="Testi mies",
            bio="Hello World!",
            email="test@test.com",
            phone="555-1234567",
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