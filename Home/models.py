from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank = True, null=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)

    def __str__(self):
        return self.name
