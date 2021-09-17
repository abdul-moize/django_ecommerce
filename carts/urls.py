"""
Carts app url mapping
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.CartsAPIView.as_view(), name="Cart Api"),
    path("<int:item_pk>/", views.CartsAPIView.as_view(), name="Cart Item Api"),
]
