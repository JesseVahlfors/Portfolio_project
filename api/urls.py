from django.urls import include, path
from rest_framework import routers

from api import views

urlpatterns = [
    path('lyns/', include(routers.urls)),
]
