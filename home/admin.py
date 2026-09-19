from django.contrib import admin

from .models import Profile, Project

# Register your models here.
admin.site.register(Profile)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "date_completed", "is_featured")
    list_editable = ("is_featured",)
    list_filter = ("is_featured", "date_completed")
    search_fields = ("title",)
