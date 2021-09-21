"""
Maps urls to views
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserAPIView.as_view(), name="user_api"),
    path("login/", views.UserAuthenticationAPIView.as_view(), name="login_api"),
]
