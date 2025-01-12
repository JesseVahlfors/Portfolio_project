from django.shortcuts import render
from django.http import HttpResponse
from home.models import Profile

def home(request):
    profile = Profile.objects.first()
    if profile and profile.bio:
        bio = profile.bio
        return HttpResponse("Welcome to my site\n" + bio)
    else:
        return HttpResponse("Welcome to my site")
