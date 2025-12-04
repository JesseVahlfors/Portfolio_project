from django.urls import path
from . import views
from .views import CompressionDemoView

urlpatterns = [
    path('', CompressionDemoView.as_view(), name='compression_demo'),
    path('compress/', views.compress_action, name='compress'),
    path('decompress/', views.decompress_action, name='decompress'),
]
