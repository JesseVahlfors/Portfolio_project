import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

@pytest.fixture
def decompress_url():
    return reverse("decompress")