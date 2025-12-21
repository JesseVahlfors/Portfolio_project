import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

@pytest.fixture
def compress_url():
    return reverse("compress")

def test_compress_action_rejects_get(client, compress_url):
    response = client.get(compress_url)
    assert response.status_code == 405

def test_compress_action_returns_stats(client, compress_url):
    response = client.post(compress_url, {
        "input_text": "hello world"
    })

    assert response.status_code == 200
    assert b"Original size:</strong> 11 bytes" in response.content
    assert b"Compressed size" in response.content

def test_compress_action_empty_input(client, compress_url):
    response = client.post(compress_url, {
        "input_text": ""
    })

    assert response.status_code == 200
    assert b"Please enter some text" in response.content

def test_compress_action_compresses_input(client, compress_url):
    response = client.post(compress_url, {
        "input_text": "Huffman coding is a data compression algorithm. Huffman coding assigns shorter codes to more frequent characters and longer codes to less frequent characters. Huffman coding is widely used in compression formats. Huffman coding works best when the input contains repeated patterns. Huffman coding reduces file size by exploiting redundancy. This example text repeats the same words again and again. This example text repeats the same words again and again. This example text repeats the same words again and again. This example text repeats the same words again and again. This example text repeats the same words again and again."
    })

    assert response.status_code == 200
    assert b"630 bytes" in response.content
    assert b"Compressed size:</strong> 0 bytes" not in response.content
    assert b"Compression ratio" in response.content

def test_compress_action_whitespace_only(client, compress_url):
    response = client.post(compress_url, {"input_text": "   \n\t"})

    assert response.status_code == 200
    assert b"Please enter some text" in response.content

def test_compress_action_missing_input_text(client, compress_url):
    response = client.post(compress_url, {})

    assert response.status_code == 200
    assert b"Please enter some text" in response.content

def test_compress_action_rejects_too_large_input(client, compress_url):
    big_text = "a" * (250 * 1024 + 1)

    response = client.post(compress_url, {"input_text": big_text})

    assert response.status_code == 200
    assert b"too long" in response.content.lower()