from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo_page, name='compression_demo'),
    path('compress/', views.compress_action, name='compress_action'),
    path("decompress/", views.decompress_action, name="decompress_action"),
]
