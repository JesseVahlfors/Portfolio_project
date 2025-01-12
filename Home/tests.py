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