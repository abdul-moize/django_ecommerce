"""
Maps urls to views
"""
from django.urls import path

from . import views

urlpatterns = [
    path("users/", views.UserAPIView.as_view(), name="user_api"),
    path("users/login/", views.UserAuthenticationAPIView.as_view(), name="login_api"),
    path("", views.TemplateUserLogin.as_view(), name="template_login"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.ProfileAPIView.as_view(), name="profile"),
    path("register/", views.TemplateRegisterUser.as_view(), name="template_register"),
]
