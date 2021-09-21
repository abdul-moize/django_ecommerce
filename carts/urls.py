"""
Carts app url mapping
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.CartsAPIView.as_view(), name="cart_api"),
    path("<int:item_pk>/", views.CartsAPIView.as_view(), name="cart_item_api"),
]
