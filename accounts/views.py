# Create your views here.
# permission_classes= (permissions.IsAuthenticated)
import json
from django.http import JsonResponse
from django_countries import countries, Countries
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from dj_rest_auth.registration.views import RegisterView

from recruiters.models import Applicants, Job
from .models import User, Profile
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    RecruiterRegisterSerializer,
    ProfileSerializer,
    MyTokenObtainPairSerializer,
)
from .permissions import IsOwnerOrReadOnly
from recruiters.serializers import (
    ApplicantSerializer,
    JobSerializer,
    SelectedSerializer,
)


class UserRegisterView(RegisterView):
    serializer_class = UserRegisterSerializer


class RecruiterRegisterView(RegisterView):
    serializer_class = RecruiterRegisterSerializer
    # queryset = Recruiter.objects.all().order_by("-id")


class UsersAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        print("This serializer ran")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """List, retreive operations for a user"""

    serializer_class = ProfileSerializer
    queryset = User.objects.all().order_by("-id")
    lookup_field = "pk"
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return UserSerializer
        elif self.action == "retrieve":
            return ProfileSerializer
        else:
            return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        try:
            instance: User = self.get_object()
            instance = instance.profile
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(instance, data=request.data, many=False)
        print(request.data)
        print(request.POST.get("user"))
        # user_data = json.loads(request.data["user"])
        # # user_data = request.data
        # # instance.username=
        # print(user_data)
        user_serializer = UserSerializer(request.user, data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        if serializer.is_valid():
            # user, data=request.data,
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        instance = self.get_object()
        # print(repr(instance), 'profile instance')
        try:
            # user = Profile.objects.get(pk=pk)
            instance = instance.profile
        except Profile.DoesNotExist as e:
            return Response(exception=True, status=status.HTTP_404_NOT_FOUND)

        print(instance, request.user)
        serializer = ProfileSerializer(instance, many=False)
        # print(serializer.data)

        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def applied(self, request, *args, **kwargs):
        user = self.get_object()
        print(request.user)
        self.serializer_class = ApplicantSerializer
        applicants = user.applied.all()
        page = self.paginate_queryset(applicants)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(applicants, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def selected(self, request, *args, **kwargs):
        job = self.get_object()
        print(request.user)

        # applicants = Applicants.objects.filter(job=job)
        # applicants = job.selected_applications.all()
        # serializer = SelectedSerializer(applicants, many=True)
        # return Response(serializer.data)

        self.serializer_class = SelectedSerializer
        applicants = job.selected_applications.all()
        page = self.paginate_queryset(applicants)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(applicants, many=True)
        return Response(serializer.data)

    # @action(
    #     detail=True, url_path="apply/(?P<id>[^/.]+)", methods=["get", "put", "delete"]
    # )
    # def apply(self, request, *args, **kwargs):
    #     # user: User = self.get_object()
    #     # self.queryset = Applicants.objects.all().order_by("-id")
    #     self.lookup_url_kwarg = "id"
    #     self.queryset = Applicants.objects.all().order_by("-id")
    #     self.serializer_class = ApplicantSerializer
    #     # instance = request.user
    #     print(repr(request.user))
    #     print(self.kwargs.get("pk"), kwargs)
    #     if not self.get_object:
    #         print(repr(self.get_object()), "first instance")
    #     # applicants = Applicants.objects.filter(job=job)
    #     # applicants = job.applicants.all()
    #     user = request.user
    #     applied = user.applied.all()
    #     print(applied)

    #     if request.method == "PUT":
    #         instance = self.get_object()
    #         if self.get_object:
    #             print(repr(self.get_object()), "instance ")
    #             instance = self.get_object()
    #         serializer = self.get_serializer(instance, data=request.data, many=False)
    #         if serializer.is_valid():
    #             serializer.save(job_id=kwargs["id"], applicant=self.request.user)
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     if request.method == "DELETE":
    #         serializer = self.get_serializer(data=request.data, many=False)
    #         if serializer.is_valid():
    #             serializer.save(job_id=kwargs["id"], applicant=self.request.user)
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     serializer = ApplicantSerializer(applied, many=True)

    #     return Response(serializer.data)


class ApplicationViewSet(viewsets.ModelViewSet):
    """Operations for users to apply"""

    serializer_class = ApplicantSerializer
    queryset = Applicants.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]

    # lookup_field = "pk"
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     job_id = self.kwargs.get("pk")
    #     user = self.request.user
    #     print(user, self.kwargs, job_id, queryset)
    #     if job_id:
    #         queryset = queryset.filter(job=job_id)
    #     print(queryset)
    #     return queryset
    def create(self, request, *args, **kwargs):
        if Applicants.objects.filter(job_id=kwargs["pk"]):
            print(self.queryset)
            return Response(
                {"detail": "You have already applied"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)

    def get_object(self):
        return super().get_object()

    def perform_create(self, serializer: ApplicantSerializer):
        # print(repr(self.get_object()))
        # self.queryset = Applicants.objects.all()
        # print(self.kwargs)
        serializer.save(job_id=self.kwargs["pk"], applicant=self.request.user)
        return super().perform_create(serializer)

    # def perform_update(self, serializer: ApplicantSerializer):
    #     print(repr(self.get_object()))
    #     # self.queryset = Applicants.objects.all()
    #     # print(self.kwargs)
    #     serializer.save(job_id=self.kwargs["pk"], applicant=self.request.user)
    #     return super().perform_update(serializer)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = ApplicantSerializer(instance, data=request.data, many=False)
    #     print(request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     # return super().update(request, *args, **kwargs)

    # def retrieve(self, request, *args, **kwargs):
    #     recruiter_pk = self.kwargs.get("username")
    #     # self.queryset = Job.objects.all()
    #     instance = self.get_object()
    #     instance = Job.objects.get(id=kwargs["pk"])
    #     print(kwargs)
    #     # instance = request.user
    #     print(instance, request.user)
    #     # serializer = ApplicantSerializer(instance, many=False)
    #     serializer = JobSerializer(instance, many=False)
    #     # print(serializer.data)
    #     return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE", "PATCH"])
# @permission_classes([IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly])
def user_profile(request, pk):
    try:
        # user = User.objects.get(pk=pk)
        user = request.user
        print(pk)
    except User.DoesNotExist or Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = UserSerializer(user, context={"request": None})
        return Response(serializer.data)
    if request.method == "PATCH":
        serializer = UserSerializer(
            user, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     student.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_profile(request, pk):
    try:
        user = request.user
    except User.DoesNotExist or Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        # user = request.user
        profile = user.profile
        print(user)
        serializer = ProfileSerializer(profile, many=False)
        print(serializer.data)
        return Response(serializer.data)

    if request.method == "POST":
        print(user)
        print(user.profile)
        # serializer = ProfileSerializer(user, data=request.data)
        serializer = ProfileSerializer(user.profile, data=request.data)
        print(serializer.initial_data)
        # print(serializer1.initial_data)
        if serializer.is_valid():
            # serializer.update(user.profile,request.data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["OPTIONS", "GET"])
@permission_classes([IsAuthenticated])
def get_countries(request):
    # country_list = [{"code": code, "name": name} for code, name in countries]
    return Response(dict(countries))
