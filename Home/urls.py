from django.urls import path
from .views import ProjectDetailView, MainView, ProjectsView, contact
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', MainView.as_view(), name='home/main_page'),
    path('projects/', ProjectsView.as_view(), name='home/projects'),
    path('contact/', contact, name='contact'),
    path('<slug:slug>/', ProjectDetailView.as_view(), name='home/project_detail')
]
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)