from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project

class MainViewSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return ['home/main_page']
    
    def location(self, item):
        return reverse(item)
    
class ProjectsViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Project.objects.all()
    
    def lastmod(self, obj):
        return obj.date_completed