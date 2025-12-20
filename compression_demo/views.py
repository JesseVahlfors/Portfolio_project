from django.shortcuts import render
from compression_tool.compressor import compress
from compression_tool.decompressor import decompress
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from home.models import Profile


class CompressionDemoView(TemplateView):
    template_name = 'compression_demo/compression_demo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        return context

@require_POST
def compress_action(request):
    input_text = request.POST.get("input_text", "")

    original_size = 0
    compressed_size = 0
    compression_ratio = 0 if original_size == 0 else round((compressed_size / original_size) * 100, 1)

    if not input_text.strip():
        summary = "Please enter some text"
    else:
        summary = f"Your original file size was {original_size} and compressed file is {compressed_size}."

    

    return render(request, 'compression_demo/_compress_results.html', {
    "original_size": original_size,
    "compressed_size": compressed_size,
    "compression_ratio": compression_ratio,
    "summary": summary
    })
    

def decompress_action(request):
    pass

