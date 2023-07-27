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
router.register(r"", views.UserViewSet)

urlpatterns = [
    # re_path(r'^api/students/$', views.students_list),
    # re_path(r'^api/students/([0-9])$', views.students_detail)
    path("<int:pk>/update/", views.user_profile, name="index"),
    path(
        "apply/<int:pk>/",
        views.ApplicationViewSet.as_view({"get": "list", "put": "create"}),
    ),
    path("", include(router.urls)),
    # path('<int:pk>/', views.get_profile),
    # path('<int:pk>/profile', views.user_profile, name='profile-detail'),
    # path('token/', views.MyTokenObtainPaisrView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
