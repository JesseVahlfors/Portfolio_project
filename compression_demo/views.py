import base64
from django.shortcuts import render
from compression_tool.compressor import compress
from compression_tool.decompressor import decompress
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from home.models import Profile
from binascii import Error as BinasciiError

MAX_TEXTAREA_BYTES = 250 * 1024 #250 kb


class CompressionDemoView(TemplateView):
    template_name = 'compression_demo/compression_demo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        return context

@require_POST
def compress_action(request):
    compress_url = 'compression_demo/_compress_results.html'  
    input_text = request.POST.get("input_text", "")

    original_size = 0
    compressed_size = 0
    compression_ratio = 0

    if not input_text.strip():
        return render(request, compress_url, {
            "compressed_b64": "",
            "original_size": 0,
            "compressed_size": None,
            "compression_ratio": None,
            "summary": "Please enter some text",
        })

    input_bytes = input_text.encode("utf-8")
    
    if len(input_bytes) > MAX_TEXTAREA_BYTES:
        return render(request, compress_url, {
            "compressed_b64": "",
            "original_size": len(input_bytes),
            "compressed_size": None,
            "compression_ratio": None,
            "summary": "Input is too long (max 250 KB).",
        })
    
    original_size = len(input_bytes)
    compressed = compress(input_bytes)
    compressed_size = len(compressed)
    
    base64_string = base64.b64encode(compressed).decode("ascii")
    
    compression_ratio = 0 if original_size == 0 else round((compressed_size / original_size) * 100, 1)
    if compression_ratio < 100:
        summary = f"Compressed to {compressed_size} bytes ({compression_ratio} % of original)."
    else:
        summary = "Compressed output is larger than the original (common for small inputs due to header overhead)."

    

    return render(request, compress_url, {
    "compressed_b64": base64_string,
    "original_size": original_size,
    "compressed_size": compressed_size,
    "compression_ratio": compression_ratio,
    "summary": summary
    })


@require_POST
def decompress_action(request):
    compressed_b64 = request.POST.get("compressed_b64", "")
    decompress_url = "compression_demo/_decompress_results.html"

    if not compressed_b64 or not compressed_b64.strip():
        return render(request, decompress_url, {
        "decompressed_text": "",
        "error": "Please paste compressed data.",
        })
    
    try:
        compressed_bytes = base64.b64decode(compressed_b64, validate=True)
    except (BinasciiError, ValueError):
        return render(request, decompress_url, {
            "decompressed_text": "",
            "error": "Invalid base64 input."
        })
    
    try:
        raw = decompress(compressed_bytes)
    except Exception:
        return render(request, decompress_url, {
            "decompressed_text": "",
            "error": "That data doesn't look like a valid JV compressed payload."
        })

    text = raw.decode("utf-8", errors="replace")

    return render(request, decompress_url, {
            "decompressed_text": text,
            "error": "",
        })

