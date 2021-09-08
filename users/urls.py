"""
Maps urls to views
"""
from django.urls import path

from . import views

urlpatterns = [
    path("add/", views.AddUser.as_view(), name="Add User"),
    path("login/", views.LoginUser.as_view(), name="Login"),
    path("update/", views.UpdateUser.as_view(), name="Update"),
    path("delete/", views.DeleteUser.as_view(), name="Update"),
]
