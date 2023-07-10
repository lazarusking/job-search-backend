from django.shortcuts import render

# Create your views here.
# permission_classes= (permissions.IsAuthenticated)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from dj_rest_auth.registration.views import RegisterView
from .models import User, Profile, Recruiter
from .serializers import UserSerializer, UserRegisterSerializer, RecruiterRegisterSerializer, ProfileSerializer, MyTokenObtainPairSerializer
from .permissions import IsOwnerOrReadOnly
from .decorators import recruiter_required, normal_user_required
from recruiters.serializers import ApplicantSerializer, SelectedSerializer


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
        print('This serializer ran')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """List, retreive operations for a user"""

    serializer_class = ProfileSerializer
    queryset = User.objects.all().order_by("-id")
    lookup_field = 'pk'

    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        elif self.action == 'retrieve':
            return ProfileSerializer
        else:
            return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # print(repr(instance.profile), 'profile instance')
            instance = instance.profile
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(
            instance, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = self.get_object()
        # print(repr(instance), 'profile instance')
        try:
            # user = Profile.objects.get(pk=pk)
            instance = instance.profile
        except Profile.DoesNotExist as e:
            return Response(exception=True, status=status.HTTP_404_NOT_FOUND)

        print(instance, request.user)
        serializer = ProfileSerializer(
            instance, many=False)
        # print(serializer.data)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def applicants(self, request, *args, **kwargs):
        user = self.get_object()
        print(request.user)

        # applicants = Applicants.objects.filter(job=job)
        applicants = user.applied.all()
        serializer = ApplicantSerializer(applicants, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def selected(self, request, *args, **kwargs):
        job = self.get_object()
        print(request.user)

        # applicants = Applicants.objects.filter(job=job)
        applicants = job.selected_applications.all()
        serializer = SelectedSerializer(applicants, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly])
def user_profile(request, pk):
    try:
        user = User.objects.get(pk=pk)
        # user = request.user
    except User.DoesNotExist or Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProfileSerializer(
            user.profile, context={'request': None})
        return Response(serializer.data)
    # if request.method == 'PUT':
    #     serializer = UserSerializer(
    #         student, data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     student.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_profile(request, pk):
    try:
        user = request.user
    except User.DoesNotExist or Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # user = request.user
        profile = user.profile
        print(user)
        serializer = ProfileSerializer(profile, many=False)
        print(serializer.data)
        return Response(serializer.data)

    if request.method == 'POST':
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
