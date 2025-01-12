from django.test import TestCase
from django.urls import reverse
from .models import Profile

class MainPageViewTests(TestCase):

    def setUp(self):
        Profile.objects.create(
            name="Jesse",
            bio="Hello World!",
            email="jesse@test.com"
        )

    def test_main_page_returns_200(self):
        response = self.client.get(reverse('home/main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to My Portfolio")

    def test_main_page_returns_bio_from_database(self):
        response = self.client.get(reverse('home/main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello World!")

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
            name="Jesse",
            bio="Hello World!",
            email="jesse@test.com",
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