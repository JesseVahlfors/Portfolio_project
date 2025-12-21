import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_demo__page_loads(client):
    url = reverse("compression_demo")
    response = client.get(url)

    assert response.status_code == 200
    assert b'JV Compression Tool' in response.content