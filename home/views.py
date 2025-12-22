from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView
from .models import Profile, Project
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.decorators.http import require_POST
import environ
import requests

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
        context["RECAPTCHA_PUBLIC_KEY"] = settings.RECAPTCHA_PUBLIC_KEY
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

@require_POST
def contact(request):
    form = ContactForm(request.POST)

    token = request.POST.get("g-recaptcha-response", "")
    context_base = {"form": form, "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY}

    if not token:
        context_base["recaptcha_error"] = "Please complete the reCAPTCHA."
        return render(request, "home/partials/contact_form.html", context_base, status=400)

    # Verify with Google
    try:
        verify = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_PRIVATE_KEY,
                "response": token,
                "remoteip": request.META.get("REMOTE_ADDR"),
            },
            timeout=10,
        ).json()
    except requests.RequestException:
        context_base["recaptcha_error"] = "Could not verify reCAPTCHA right now. Please try again."
        return render(request, "home/partials/contact_form.html", context_base, status=502)

    if not verify.get("success"):
        context_base["recaptcha_error"] = "reCAPTCHA verification failed. Please try again."
        return render(request, "home/partials/contact_form.html", context_base, status=400)

    if not form.is_valid():
        return render(request, "home/partials/contact_form.html", context_base, status=400)

    name = form.cleaned_data["name"]
    email = form.cleaned_data["email"]
    message = form.cleaned_data["message"]

    email_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    try:
        msg = EmailMessage(
            subject=f"Contact Form Submission from {name}",
            body=email_body,
            from_email=env("DEFAULT_FROM_EMAIL"),
            to=[env("MY_EMAIL")],
            reply_to=[email],
        )
        msg.send(fail_silently=False)

        return render(
            request,
            "home/partials/contact_form.html",
            {
                "form": ContactForm(),
                "success": True,
                "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
            },
        )
    except Exception:
        return render(
            request,
            "home/partials/contact_form.html",
            {
                "form": form,
                "email_error": "Email sending failed. Please try again.",
                "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
            },
            status=500,
        )