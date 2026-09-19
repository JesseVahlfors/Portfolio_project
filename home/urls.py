from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.generic import RedirectView

from .sitemaps import MainViewSitemap, ProjectsViewSitemap
from .views import MainView, ProjectDetailView, ProjectsView, contact

sitemaps = {
    "main": MainViewSitemap,
    "projects": ProjectsViewSitemap,
}

urlpatterns = [
    path("", MainView.as_view(), name="home/main_page"),
    path("contact/", contact, name="contact"),
    path("projects/", ProjectsView.as_view(), name="home/projects"),
    path(
        "projects/<slug:slug>/", ProjectDetailView.as_view(), name="home/project_detail"
    ),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
