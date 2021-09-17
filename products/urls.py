"""
Contains url mapping for products app
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products import views

router = DefaultRouter()
router.register(r"", views.ProductViewSet)

urlpatterns = [path("", include(router.urls))]
