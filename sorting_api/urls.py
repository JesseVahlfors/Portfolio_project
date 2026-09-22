from django.urls import path

from .views import SortingView

urlpatterns = [
    path("sort/", SortingView.as_view(), name="sort"),
]
