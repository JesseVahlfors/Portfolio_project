from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView
from .models import Profile, Project
from .forms import ContactForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
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
        context["is_main_page"] = True
        context["form"] = ContactForm()
        return context
    
   
class ProjectsView(ListView):
    model = Project
    template_name = 'home/project_list.html'
    context_object_name = 'projects'
    ordering = ['-date_completed']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'home/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        project = context['project']
        context["profile"] = Profile.objects.first()
        context["is_main_page"] = False

        skills = project.skills
        if skills:
            context["skills"] = skills.split(',')
        else:
            context["skills"] = None
        return context

    def get_object(self):
        return get_object_or_404(Project, slug=self.kwargs['slug'])
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            try:
                send_mail(
                    f"Contact Form Submission from {name}",
                    message,
                    email,  # From email
                    [env('MY_EMAIL')],  # Replace with your email address or settings
                    fail_silently=False,
                ) 
                return JsonResponse({'message': 'Thanks for contacting me!'})
            except Exception as e:
                return JsonResponse({'errors': {'email': str(e)}}, status=500)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    form = ContactForm()      
    return render(request, 'home/main_page.html', {'form': form})
    