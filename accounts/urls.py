from django.urls import path, include
from rest_framework import routers

from . import views


def create_router(route, viewset):
    router = routers.DefaultRouter()
    router.register(r"{}".format(route), viewset)
    return router


app_name = "accounts"
user_router = create_router("", views.UserViewSet)
router = routers.DefaultRouter()

# router.register(r"apply", views.ApplicationViewSet, basename="apply")
# router.register(r"saved", views.SavedJobList)
router.register(r"", views.UserViewSet)

urlpatterns = [
    # re_path(r'^api/students/$', views.students_list),
    # re_path(r'^api/students/([0-9])$', views.students_detail)
    path("<int:pk>/update/", views.user_profile, name="index"),
    path(
        "apply/<int:pk>/",
        views.ApplicationViewSet.as_view(
            {"get": "list", "post": "create", "delete": "destroy"}
        ),
    ),
    path(
        "saved/<int:pk>/",
        views.SavedJobViewSet.as_view(
            {"get": "list", "post": "create", "delete": "destroy"}
        ),
    ),
    path("applied/", views.AppliedList.as_view()),
    path("selected/", views.SelectedList.as_view()),
    # path("saved/", views.SavedJobList.as_view()),
    path("", include(router.urls)),
]
