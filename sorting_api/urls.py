from django.urls import path
from . import views

urlpatterns = [
    path('bubble-sort/', BubbleSortView.as_view(), name='bubble-sort'),
]
