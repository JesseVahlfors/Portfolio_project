import pytest
import base64
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_demo__page_loads(client):
    url = reverse("compression_demo")
    response = client.get(url)

    assert response.status_code == 200
    assert b'JV Compression Tool' in response.content

def _extract_textarea_value(html: str, textarea_id: str):
    """ 
    Extract inner text of a <textarea id="...">
    """
    marker = f'id="{textarea_id}"'
    i = html.find(marker)
    assert i != -1, f"Expected textarea with id={textarea_id}"

    tag_start = html.rfind("<textarea", 0, i)
    assert tag_start != -1, f"Expected <textarea ...> start tag"

    content_start = html.find(">", tag_start) + 1
    assert content_start != 0, f"Expected end of <textarea ...> openin tag"

    content_end = html.find("</textarea>", content_start)
    assert content_end != -1, f"Expected </textarea> closing tag"

    return html[content_start:content_end].strip()

def test_roundtrip_compress_then_decompress(client):
    compress_url = reverse("compress")
    decompress_url = reverse("decompress")

    original_text = "Huffman coding is a data compression algorithm. It works best when the input contains repeated patterns. Huffman coding, Huffman coding, Huffman coding!"  

    # Compress (HTTP)
    compress_response = client.post(compress_url, {"input_text": original_text})
    assert compress_response.status_code == 200
    
    compress_html = compress_response.content.decode("utf-8")
    compressed_b64 = _extract_textarea_value(compress_html, "compressed-b64-output")
    assert compressed_b64

    # Decompress (HTTP)
    decompress_response = client.post(decompress_url, {"compressed_b64": compressed_b64})
    assert decompress_response.status_code == 200

    decompress_html = decompress_response.content.decode("utf-8")
    roundtrip_test = _extract_textarea_value(decompress_html, "decompressed-text-output")

    assert roundtrip_test == original_text