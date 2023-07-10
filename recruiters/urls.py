from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from . import views

app_name = "recruiter"


def create_router(route, viewset):
    router = routers.DefaultRouter()
    router.register(r'{}'.format(route), viewset)
    return router

router = routers.DefaultRouter()

router.register(r'jobs', views.JobsViewSet)
router.register(r'', views.RecruitersView)
# router.register(r'applicants', views.ApplicantsView)
# rec_router = create_router('', views.RecruitersView)
# job_router = create_router('jobs', views.JobsViewSet)
# applicant_router = create_router(r'applicants', views.ApplicantsView)
urlpatterns = [
    # path('', views.JobAPIView.as_view(), name="index"),
    path('', include(router.urls)),
    # path('<str:recruiter_pk>/', include(job_router.urls)),
    # path('jobs/<int:id>/', views.ApplicantsAPIView.as_view(), name="users"),
    path('search/', views.job_search_list, name="search"),
]