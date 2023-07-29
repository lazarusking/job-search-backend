import datetime

from autoslug import AutoSlugField

# Create your models here.
# from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models

# from django_countries.fields import CountryField
from django.utils import timezone

from accounts.models import User

CHOICES = (
    ("Full Time", "Full Time"),
    ("Part Time", "Part Time"),
    ("Internship", "Internship"),
    ("Remote", "Remote"),
)


class Job(models.Model):
    recruiter = models.ForeignKey(User, related_name="jobs", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # company = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    skills_required = models.CharField(max_length=200)
    job_type = models.CharField(
        max_length=30, choices=CHOICES, default="Full Time", null=True
    )
    link = models.URLField(blank=True)
    slug = AutoSlugField(populate_from="title", unique=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_company(self):
        return self.recruiterprofile.company

    @admin.display(
        boolean=True,
        ordering="date_posted",
        description="Expired?",
    )
    def has_job_expired(self):
        now = timezone.now()
        return now > self.deadline

    def job_extra_details(self):
        now = timezone.now()
        two_days_ago = now - datetime.timedelta(days=2)
        new_users = self.applicants.filter(date_posted__gte=two_days_ago).count()
        return {
            "id": self.id,
            "title": self.title,
            "user_count": self.applicants.count(),
            "new_users": new_users,
            "job_type": self.job_type,
            "location": self.location,
        }

    def get_absolute_url(self):
        return "/job/{}".format(self.slug)


class Applicants(models.Model):
    job = models.ForeignKey(Job, related_name="applicants", on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name="applied", on_delete=models.CASCADE
    )
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "applicants"

    def __str__(self):
        return self.applicant.username


class Selected(models.Model):
    job = models.ForeignKey(Job, related_name="selected", on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name="selected_applications", on_delete=models.CASCADE
    )
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "selected"

    def __str__(self):
        return self.applicant.username


class SavedJobs(models.Model):
    job = models.ForeignKey(Job, related_name="saved_job", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="saved", on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "job"], name="unique_saved_jobs")
        ]

    def __str__(self):
        return self.job.title
