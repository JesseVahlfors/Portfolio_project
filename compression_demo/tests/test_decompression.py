import pytest
import base64
from django.urls import reverse

pytestmark = pytest.mark.django_db

@pytest.fixture
def decompress_url():
    return reverse("decompress")

def test_decompress_rejects_get(client, decompress_url):
    response = client.get(decompress_url)

    assert response.status_code == 405

def test_decompress_missing_payload(client, decompress_url):
    response = client.post(decompress_url, {"compressed_b64": "not/base64!!!"})

    assert response.status_code == 200
    assert b"Invalid base64" in response.content

def test_decompress_invalid_base64(client, decompress_url):
    response = client.post(decompress_url, {"compressed_b64": "not-base64!!!"})

    assert response.status_code == 200
    assert b"Invalid base64" in response.content

def test_decompress_roundtrip(client, decompress_url):
    from compression_tool import compress_bytes as compress

    original = "hello world"
    compressed = compress(original.encode("utf-8"))
    payload = base64.b64encode(compressed).decode("ascii")

    response = client.post(decompress_url, {"compressed_b64": payload})

    assert response.status_code == 200
    assert b"hello world" in response.content