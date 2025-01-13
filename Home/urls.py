from django.urls import path
from .views import ProfileView, MainView, ProjectsView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', MainView.as_view(), name='home/main_page'),
    path('profile/', ProfileView.as_view(), name='home/profile'),
    path('projects/', ProjectsView.as_view(), name='home/projects'),
]
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)