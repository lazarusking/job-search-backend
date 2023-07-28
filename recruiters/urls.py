from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from . import views

app_name = "recruiter"


def create_router(route, viewset):
    router = routers.DefaultRouter()
    router.register(r"{}".format(route), viewset)
    return router


router = routers.DefaultRouter()

# router.register(r"jobs/<int:pk>/select", views.SelectionViewSet)
router.register(r"jobs", views.JobsViewSet)
# router.register(r"select", views.SelectionViewSet)
router.register(r"", views.RecruitersView)

applicant_router = create_router(r"", views.SelectionViewSet)
urlpatterns = [
    # path('', views.JobAPIView.as_view(), name="index"),
    # path("jo/<int:pk>/select/<int:user_id>/", include(applicant_router.urls)),
    path(
        "jobs/<int:pk>/select/<int:user_id>/",
        views.SelectionViewSet.as_view(
            {"get": "list", "put": "create", "delete": "destroy"}
        ),
    ),
    path("", include(router.urls)),
    # path('<str:recruiter_pk>/', include(job_router.urls)),
    # path('jobs/<int:id>/', views.ApplicantsAPIView.as_view(), name="users"),
    path("search/", views.job_search_list, name="search"),
]
