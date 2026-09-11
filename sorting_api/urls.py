from django.urls import path
from .views import BubbleSortView

urlpatterns = [
    path('bubble-sort/', BubbleSortView.as_view(), name='bubble-sort'),
]
