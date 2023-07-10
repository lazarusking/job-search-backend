
# Create your models here.
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin, Group, Permission
from django.utils import timezone
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    MinLengthValidator,
)
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField


class User(AbstractUser):
    email = models.EmailField(
        max_length=255, blank=True, null=True, unique=True)
    # phone_number = PhoneNumberField(blank=True, null=True)
    is_recruiter = models.BooleanField(
        "recruiter status",
        default=False,
        help_text="Designates whether the user is a recruiter.",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self) -> str:
        return self.username

    def set_recruiter(self):
        self.is_recruiter = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        self.email = self.email.lower()
        self.username = self.username.lower()
        # print(self.username,' lowered')

    def save(self, *args, **kwargs):
        # print(self.username, 'before save')
        super().full_clean()
        super().save(*args, **kwargs)


#     # class Meta:
#     #     db_table = 'user'
#     #     ordering = ('-first_name',)

class Recruiter(User):
    # is_recruiter = models.BooleanField(
    #     "recruiter status",
    #     default=True,
    #     help_text="Designates whether the user is a recruiter.",
    # )

    class Meta:
        db_table = 'recruiter'

    def clean(self):
        self.set_recruiter()
        super().clean()

    def set_recruiter(self):
        self.is_recruiter = True

    def save(self, *args, **kwargs):
        self.set_recruiter()
        super().save(*args, **kwargs)


class Profile(models.Model):
    GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
    )
    CHOICES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    )

    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='user', unique=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    description = models.TextField(default="", blank=True)
    country = CountryField(blank_label="(select country)", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    gender = models.CharField(
        max_length=255, blank=True, null=True, choices=GENDER)

    address = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(
        validators=[MaxValueValidator(timezone.now().date())], blank=True, null=True
    )
    looking_for = models.CharField(
        max_length=30, choices=CHOICES, default='Full Time', null=True)
    resume = models.FileField(upload_to="resumes/", blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    linkedin = models.URLField(max_length=256, blank=True)
    facebook = models.URLField(max_length=255, blank=True)
    github = models.URLField(max_length=255, blank=True)
    website = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return "/profile/{}".format(self.slug)

    def calculate_age(self):
        today = timezone.now()
        born = self.date_of_birth
        self.age = (
            today.year - born.year -
            ((today.month, today.day) < (born.month, born.day))
        )


# foreign key is User instead of Recruiter to allow
# admin form's inline model to refer to User


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='user', unique=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    company = models.CharField(max_length=200, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    description = models.TextField(default="", blank=True)
    country = CountryField(blank_label="(select country)", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=50, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    linkedin = models.URLField(max_length=256, blank=True)
    facebook = models.URLField(max_length=255, blank=True)
    github = models.URLField(max_length=255, blank=True)
    website = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return "users/{}/profile/".format(self.slug)


@receiver(post_save, sender=User)
@receiver(post_save, sender=Recruiter)
def create_user_profile(sender, instance, created, **kwargs):
    print('***', created, instance.is_recruiter)
    print(repr(instance))
    # if created:
    #     if hasattr(instance, 'is_recruiter') and instance.is_recruiter:
    #         RecruiterProfile.objects.create(user=instance)
    #     else:
    #         Profile.objects.create(user=instance)
    if created:
        if instance.is_recruiter:
            RecruiterProfile.objects.create(user=instance)
        else:
            Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
@receiver(post_save, sender=Recruiter)
def save_user_profile(sender, instance, created, **kwargs):
    # if hasattr(instance, 'is_recruiter') and instance.is_recruiter:
    #     # RecruiterProfile.objects.get_or_create(user=instance)
    #     instance.recruiterprofile.save()
    # else:
    #     instance.profile.save()
    if instance.is_recruiter:
        instance.recruiterprofile.save()
    else:
        instance.profile.save()
