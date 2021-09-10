"""
Maps urls to views
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserAPIView.as_view(), name="User Api"),
    path("login/", views.LoginUser.as_view(), name="Login User"),
]
