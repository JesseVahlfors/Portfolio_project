from django.shortcuts import render
from compression_tool.compressor import compress
from compression_tool.decompressor import decompress
from django.views.generic import TemplateView
from home.models import Profile

class CompressionDemoView(TemplateView):
    template_name = 'compression_demo/compression_demo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        return context

def compress_action(request):
    pass

def decompress_action(request):
    pass

