from django.shortcuts import render, redirect 
from django.views.generic import DetailView, TemplateView, ListView
from .models import Profile, Project
from .forms import ContactForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
import environ

env = environ.Env()
environ.Env.read_env()

class MainView(TemplateView):
    template_name = 'home/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        context["projects"] = Project.objects.all()[:3]
        if Profile.objects.first() and Profile.objects.first().skills:
            context["skills"] = Profile.objects.first().skills.split(',')
        return context
    
   
class ProfileView(DetailView):
    model = Profile
    template_name = 'home/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.first()
    
class ProjectsView(ListView):
    model = Project
    template_name = 'home/project_list.html'
    context_object_name = 'projects'
    ordering = ['-date_completed']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        return context
    
def contact(request):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']

                send_mail(
                    f"Contact Form Submission from {name}",
                    message,
                    email,
                    [env('MY_EMAIL')],
                    fail_silently=False,
                )

                return HttpResponseRedirect('/#contact')
            
        else:
            form = ContactForm()
        return render(request, 'home/main_page.html', {'form': form})
    