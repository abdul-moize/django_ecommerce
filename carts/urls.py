"""
Carts app url mapping
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.CartsAPIView.as_view(), name="cart_api"),
    path("detail/", views.TemplateCartsAPIView.as_view(), name="cart"),
    path("orders/", views.TemplateViewCarts.as_view(), name="orders"),
    path("<int:item_pk>/", views.CartsAPIView.as_view(), name="cart_item_api"),
]
