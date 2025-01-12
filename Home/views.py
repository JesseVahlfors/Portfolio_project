from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from .models import Profile

class MainView(TemplateView):
    template_name = 'home/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        return context

        
class ProfileView(DetailView):
    model = Profile
    template_name = 'home/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.first()
