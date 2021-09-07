from django.urls import path

from . import views

urlpatterns = [
    path('add_user/', views.AddUser.as_view(), name='index'),
]