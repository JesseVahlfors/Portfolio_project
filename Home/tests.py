from django.test import TestCase
from django.urls import reverse

class HomeIndexViewTests(TestCase):
    def test_index_page_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to my site")