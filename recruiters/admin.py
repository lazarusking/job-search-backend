from django.contrib import admin

# Register your models here.
from .models import Job, Applicants, Selected


class JobAdmin(admin.ModelAdmin):
    list_display = ["title", "has_job_expired"]
    list_filter = ["date_posted"]
    search_fields=["title"]


admin.site.register(Job, JobAdmin)
admin.site.register(Selected)
admin.site.register(Applicants)
