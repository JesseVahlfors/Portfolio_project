import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_demo__page_loads(client):
    url = reverse("compression_demo")
    response = client.get(url)

    assert response.status_code == 200
    assert b'JV Compression Tool' in response.content

def test_compress_action_rejects_get(client):
    url = reverse("compress")
    response = client.get(url)
    assert response.status_code == 405

def test_compress_action_returns_stats(client):
    url = reverse("compress")

    response = client.post(url, {
        "input_text": "hello world"
    })

    assert response.status_code == 200
    assert b"Original size:</strong> 11 bytes" in response.content
    assert b"Compressed size" in response.content

def test_compress_action_empty_input(client):
    url = reverse("compress")

    response = client.post(url, {
        "input_text": ""
    })

    assert response.status_code == 200
    assert b"Please enter some text" in response.content

def test_compress_action_compresses_input(client):
    url = reverse("compress")

    response = client.post(url, {
        "input_text": "Huffman coding is a data compression algorithm. Huffman coding assigns shorter codes to more frequent characters and longer codes to less frequent characters. Huffman coding is widely used in compression formats. Huffman coding works best when the input contains repeated patterns. Huffman coding reduces file size by exploiting redundancy. This example text repeats the same words again and again. This example text repeats the same words again and again. This example text repeats the same words again and again. This example text repeats the same words again and again. This example text repeats the same words again and again."
    })

    assert response.status_code == 200
    assert b"630 bytes" in response.content
    assert b"Compressed size:</strong> 0 bytes" not in response.content