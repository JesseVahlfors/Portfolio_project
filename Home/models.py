from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(max_length=255)
    email = models.EmailField((""), max_length=254)
    phone = models.CharField(max_length=15, blank = True, null=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
