from django.urls import path
from django.views.generic import RedirectView
from .views import ProjectDetailView, MainView, ProjectsView, contact
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', MainView.as_view(), name='home/main_page'),
    path('contact/', contact, name='contact'),
    path('projects/', RedirectView.as_view(url='/', permanent=True)),
    #path('projects/', ProjectsView.as_view(), name='home/projects'), 
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='home/project_detail'),
]
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:  # Serve static files in production
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)