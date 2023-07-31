from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import status
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from accounts import permissions
from .models import Job, Applicants, Selected
from .permissions import IsNotRecruiter, IsOwner, IsJobOwner, IsRecruiterOrReadOnly
from .serializers import JobSerializer, ApplicantSerializer, SelectedSerializer
from .decorators import recruiter_required, normal_user_required
from accounts.models import Recruiter, User
from accounts.serializers import (
    UserSerializer,
    RecruiterSerializer,
    ProfileSerializer,
    RecruiterProfile,
    RecruiterProfileSerializer,
)


# @api_view(['GET'])
# @method_decorator([recruiter_required],name='dispatch')
class JobsViewSet(viewsets.ModelViewSet):
    """List, retreive operations for a job"""

    serializer_class = JobSerializer
    queryset = Job.objects.all().order_by("-id")
    permission_classes = [IsRecruiterOrReadOnly, IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "location", "recruiter__username"]

    def get_permissions(self):
        if self.action in ["list", "detail","retrieve"]:
            print("list view runs")
            permission_classes = [AllowAny]
            return [permission() for permission in permission_classes]
        # elif self.action in ["create", "destroy", "update"]:
        #     permission_classes = [IsRecruiterOrReadOnly]
        #     return [permission() for permission in permission_classes]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)
        return super().perform_create(serializer)

    # def get_object(self):
    #     return self.request.user.recruiterprofile
    #     return super().get_object()
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     recruiter_pk = self.kwargs.get('recruiter_pk')
    #     user = self.request.user
    #     # print(user, recruiter_pk, queryset)
    #     if recruiter_pk:
    #         queryset = queryset.filter(recruiter__username=recruiter_pk)
    #     return queryset

    @action(detail=False, methods=["get"])
    def details(self, request, *args, **kwargs):
        queryset = super().get_queryset()
        final_list = []
        for i in queryset:
            extra = i.job_extra_details()
            final_list.append(extra)
        paginator = Paginator(final_list, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "jobs": final_list,
        }
        return Response(final_list)

    @action(detail=True, methods=["get"])
    def applicants(self, request, *args, **kwargs):
        job = self.get_object()
        print(request.user)

        self.serializer_class = ApplicantSerializer
        applicants = job.applicants.all().order_by("-id")
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
        # applicants = job.selected.all()
        # print(repr(applicants))
        # serializer = SelectedSerializer(applicants, many=True)
        # return Response(serializer.data)

        self.serializer_class = SelectedSerializer
        applicants = job.selected.all().order_by("-id")
        page = self.paginate_queryset(applicants)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(applicants, many=True)
        return Response(serializer.data)

    # @action(
    #     detail=True, url_path="select/(?P<id>[^/.]+)", methods=["get", "put", "delete"]
    # )
    # def select(self, request, pk=None, *args, **kwargs):
    #     job = self.get_object()
    #     print(request.user)
    #     print(self.kwargs, kwargs)
    #     self.lookup_url_kwarg = "pk"
    #     self.queryset = Selected.objects.all().order_by("-id")
    #     self.serializer_class = SelectedSerializer
    #     print(repr(self.get_object()), repr(job))
    #     user = self.get_object()

    #     if request.method == "PUT":
    #         serializer = SelectedSerializer(user, data=request.data, many=False)
    #         if serializer.is_valid():
    #             serializer.save(job=job, applicant_id=self.kwargs["id"])
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     applicants = job.selected.all().order("-id")
    #     print(repr(applicants))
    #     serializer = SelectedSerializer(applicants, many=True)
    #     return Response(serializer.data)


class SelectionViewSet(viewsets.ModelViewSet):
    """Operations for recruiters to select applicant"""

    serializer_class = SelectedSerializer
    queryset = Selected.objects.all().order_by("-id")
    lookup_field = "applicant_id"
    lookup_url_kwarg = "user_id"
    permission_classes = [IsOwner, IsAuthenticated]

    # def get_permissions(self):
    #     if self.action == "create":
    #         permission_classes = [IsNotRecruiter]
    #         return [permission() for permission in permission_classes]

    #     return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        print(kwargs)
        print(self.action)
        print(self.queryset)
        print(self.queryset)
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        print(kwargs)
        get_object_or_404(User, id=kwargs["user_id"])
        if Selected.objects.filter(job_id=kwargs["pk"], applicant_id=kwargs["user_id"]):
            return Response(
                {"detail": "You have already selected this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer: SelectedSerializer):
        # self.queryset = Job.objects.all().order_by("-id")
        # user = self.get_object()
        serializer.save(job_id=self.kwargs["pk"], applicant_id=self.kwargs["user_id"])
        return super().perform_create(serializer)


class RecruitersView(viewsets.ModelViewSet):
    """Operations for recruiters"""

    serializer_class = RecruiterProfileSerializer
    queryset = User.objects.all().filter(is_recruiter=True).order_by("-id")
    # lookup_field = "username"
    permission_classes = [IsOwner]

    def get_serializer_class(self):
        if self.action == "list":
            return RecruiterSerializer
        elif self.action == "retrieve":
            return RecruiterProfileSerializer
        else:
            return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RecruiterProfileSerializer(
            instance.recruiterprofile, data=request.data, many=False
        )
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        recruiter_pk = self.kwargs.get("username")
        instance = self.get_object()  # get current object with lookup field
        # instance = request.user # get current auth user
        print(instance.recruiterprofile, request.user)
        serializer = RecruiterProfileSerializer(instance.recruiterprofile, many=False)
        # print(serializer.data)
        return Response(serializer.data)


@api_view(["GET"])
def job_search_list(request):
    query = request.GET.get("p")
    loc = request.GET.get("q")
    object_list = []
    print(query, loc)
    if query == None:
        object_list = Job.objects.all()
    else:
        title_list = Job.objects.filter(title__icontains=query).order_by("-date_posted")
        skill_list = Job.objects.filter(skills_required__icontains=query).order_by(
            "-date_posted"
        )
        company_list = RecruiterProfile.objects.filter(
            company__icontains=query
        ).order_by("-date_posted")
        job_type_list = Job.objects.filter(job_type__icontains=query).order_by(
            "-date_posted"
        )
        for i in title_list:
            object_list.append(i)
        for i in skill_list:
            if i not in object_list:
                object_list.append(i)
        for i in company_list:
            if i not in object_list:
                object_list.append(i)
        for i in job_type_list:
            if i not in object_list:
                object_list.append(i)
    if loc == None:
        locat = Job.objects.all()
    else:
        locat = Job.objects.filter(location__icontains=loc).order_by("-date_posted")
    final_list = []
    for i in object_list:
        if i in locat:
            final_list.append(i)
    paginator = Paginator(final_list, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "jobs": page_obj,
        "query": query,
    }
    return Response(context)
