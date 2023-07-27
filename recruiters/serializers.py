from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from accounts.serializers import UserSerializer

from .models import Applicants, Job, Selected

User = get_user_model()


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["recruiter"]

        # fields = ['slug','title', 'company', 'location',
        #           'description', 'skills_required', 'job_type', 'link', 'date_posted','deadline']
        help_texts = {
            "skills_required": "Enter all the skills required each separated by commas.",
            "link": "If you want candidates to apply on your company website rather than on our website, please provide the link where candidates can apply. Otherwise, please leave it blank or candidates would not be able to apply directly!",
        }


class ApplicantSerializer(serializers.ModelSerializer):
    job = JobSerializer(
        many=False,
        read_only=True,
        validators=[
            UniqueValidator(
                queryset=Job.objects.all(),
                message="Already applied",
                lookup="iexact",
            )
        ],
    )
    applicant = UserSerializer(
        read_only=True,
        validators=[
            UniqueValidator(
                queryset=Applicants.objects.all(),
                message="Already applied",
                lookup="iexact",
            )
        ],
    )

    class Meta:
        model = Applicants
        fields = "__all__"
        depth = 1


class SelectedSerializer(serializers.ModelSerializer):
    job = JobSerializer(many=False, read_only=True)
    applicant = UserSerializer(read_only=True)

    class Meta:
        model = Selected
        fields = "__all__"


# class JobUpdateForm(serializers.ModelSerializer):
#     class Meta:
#         model = Job
#         fields = ['title', 'company', 'location',
#                   'description', 'skills_required', 'job_type', 'link', 'date_posted']
#         help_texts = {
#             'skills_req': 'Enter all the skills required each separated by commas.',
#             'link': 'If you want candidates to apply on your company website rather than on our website, please provide the link where candidates can apply. Otherwise, please leave it blank or candidates would not be able to apply directly!',
#         }
