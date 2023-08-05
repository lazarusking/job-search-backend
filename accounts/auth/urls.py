from django.urls import path, re_path
from dj_rest_auth.registration.views import (
    RegisterView,
    VerifyEmailView,
    ConfirmEmailView,
)
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Normal User Auth
    path("login/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Recruiter Auth
    path(
        "login/recruiter/",
        views.MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("register/recruiter/", views.RecruiterRegisterView.as_view()),
    path("register/", views.UserRegisterView.as_view()),
    path("account-confirm-email/<str:key>/", ConfirmEmailView.as_view()),
    #    path('login/', LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path(
        "account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("password-reset/", PasswordResetView.as_view()),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
