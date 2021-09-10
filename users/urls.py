"""
Maps urls to views
"""
from django.urls import path

from . import views

urlpatterns = [path("", views.UserAPI.as_view(), name="User Api")]
