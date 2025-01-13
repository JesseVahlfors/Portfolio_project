from django.urls import path
from .views import ProfileView, MainView, ProjectsView

urlpatterns = [
    path('', MainView.as_view(), name='home/main_page'),
    path('profile/', ProfileView.as_view(), name='home/profile'),
    path('projects/', ProjectsView.as_view(), name='home/projects'),
]
    