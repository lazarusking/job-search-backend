from django.db import models

# Create your models here.
# from django.contrib.auth.models import User
from django.contrib import admin
from accounts.models import User, Recruiter
from django.utils import timezone
from autoslug import AutoSlugField
# from django_countries.fields import CountryField
from django.utils import timezone

CHOICES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Internship', 'Internship'),
    ('Remote', 'Remote'),
)


class Job(models.Model):
    recruiter = models.ForeignKey(
        User, related_name='jobs', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # company = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    skills_required = models.CharField(max_length=200)
    job_type = models.CharField(
        max_length=30, choices=CHOICES, default='Full Time', null=True)
    link = models.URLField(blank=True)
    slug = AutoSlugField(populate_from='title', unique=True, null=True)
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

    def get_absolute_url(self):
        return "/job/{}".format(self.slug)


class Applicants(models.Model):
    job = models.ForeignKey(
        Job, related_name='applicants', on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name='applied', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'applicants'

    def __str__(self):
        return self.applicant.username


class Selected(models.Model):
    job = models.ForeignKey(
        Job, related_name='selected', on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name='selected_applications', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'selected'

    def __str__(self):
        return self.applicant.username
