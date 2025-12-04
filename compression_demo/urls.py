from django.urls import path
from . import views

urlpatterns = [
    path('', views.compression_demo_page, name='json_parser'),
    path('compress/', views.compress_action, name='compress'),
    path('decompress/', views.decompress_action, name='decompress'),
]
