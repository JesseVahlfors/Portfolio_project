from django.urls import path
from .views import ProfileView, MainView

urlpatterns = [
    path('', MainView.as_view(), name='home/main_page'),
    path('profile/', ProfileView.as_view(), name='home/profile')
]
    