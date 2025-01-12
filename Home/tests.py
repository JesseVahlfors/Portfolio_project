from django.test import TestCase
from django.urls import reverse
from home.models import Profile

class HomeIndexViewTests(TestCase):

    def setUp(self):
        Profile.objects.create(
            name="Jesse",
            bio="Hello World!",
            email="jesse@test.com"
        )

    def test_index_page_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to my site")

    def test_index_page_returns_bio_from_database(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello World!")