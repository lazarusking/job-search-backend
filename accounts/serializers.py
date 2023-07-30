from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django_countries.serializers import CountryFieldMixin
from django.contrib.auth import get_user_model
from django.db import transaction
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Profile, RecruiterProfile

User = get_user_model()


class UserRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=32,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with this email already exists",
                lookup="iexact",
            )
        ],
    )
    username = serializers.CharField(
        # validators=[UniqueValidator(
        #     queryset=User.objects.all(), message='A user with this username already exists', lookup='iexact')]
    )
    password1 = serializers.CharField(min_length=8, write_only=True, required=True)
    password2 = serializers.CharField(min_length=8, write_only=True, required=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value):
        # value = value.lower()
        # print(User.objects.get(username__iexact=value).exists())
        if User.objects.filter(username__iexact=value).exists():
            print(User.objects.filter(username__iexact=value).exists())

            raise serializers.ValidationError(
                "A user with this username already exists"
            )
        return value

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match"}
            )
        return attrs

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        # print(data, self.validated_data)
        data["first_name"] = self.validated_data["first_name"]
        data["last_name"] = self.validated_data["last_name"]
        return data

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
            validated_data["first_name"],
            validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        return user


class RecruiterRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=32,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with this email already exists",
                lookup="iexact",
            )
        ],
    )
    username = serializers.CharField(
        # validators=[UniqueValidator(
        #     queryset=User.objects.all(), message='A user with this username already exists', lookup='iexact')]
    )
    password1 = serializers.CharField(min_length=8, write_only=True, required=True)
    password2 = serializers.CharField(min_length=8, write_only=True, required=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value):
        # value = value.lower()
        # print(User.objects.get(username__iexact=value).exists())
        if User.objects.filter(username__iexact=value).exists():
            print(User.objects.filter(username__iexact=value).exists())

            raise serializers.ValidationError(
                "A user with this username already exists"
            )
        return value

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match"}
            )
        return attrs

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        print(data, self.validated_data)
        data["is_recruiter"] = True
        data["first_name"] = self.validated_data["first_name"]
        data["last_name"] = self.validated_data["last_name"]
        return data

    # def create(self, validated_data):
    #     # password = validated_data.pop('password')
    #     print(validated_data)
    #     user = User.objects.create_user(**validated_data)
    #     user.is_recruiter = True
    #     # user.set_password(password)
    #     # RecruiterProfile.objects.create(user=user)
    #     user.save()
    #     return user
    # # @transaction.atomic
    # # def save(self, request):
    # #     user = super().save(request)
    # #     user.is_recruiter = True
    # #     # RecruiterProfile.objects.create(user=user)
    # #     user.save()
    # #     return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name="index", read_only=True, lookup_field="id"
    )

    class Meta:
        model = User
        fields = (
            "url",
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_recruiter",
        )
        extra_kwargs = {"url": {"lookup_field": "id"}}
        read_only_fields = ["email", "is_recruiter"]


class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class ProfileSerializer(CountryFieldMixin, serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    url = serializers.HyperlinkedRelatedField(
        view_name="profile-detail", read_only=True, lookup_field="slug"
    )

    # avatar = serializers.ImageField()
    # resume = serializers.FileField()
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ["created_at"]

    # def update(self, instance:Profile, validated_data):
    #     print(repr(instance))
    #     print(validated_data)
    #     print(instance.user)
    #     return super().update(instance, validated_data)

    # fields = ('user', 'first_name', 'last_name', 'email')


class RecruiterProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    user = RecruiterSerializer(many=False, read_only=True)
    # url = serializers.HyperlinkedRelatedField(
    #     view_name="rec-profile-detail", read_only=True, lookup_field='username'
    # )

    class Meta:
        model = RecruiterProfile
        fields = "__all__"

    # def update(self, instance, validated_data):
    #     userprofile_instance = instance.recruiterprofile
    #     userprofile_data = validated_data.pop('user',{})
    #     print(userprofile_instance)
    #     print(userprofile_data)
    #     return super().update(instance,validated_data)

    # fields = ('user', 'slug', 'phone_number', 'company')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["is_recruiter"] = user.is_recruiter
        return token
