"""
Contains url mapping for products app
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products import views

router = DefaultRouter()
router.register(r"", views.ProductViewSet)

urlpatterns = [
    path("", views.ProductHomePageView.as_view(), name="homepage"),
    path("<int:product_pk>/", views.ProductView.as_view(), name="homepage"),
    path("add/", views.AddProductView.as_view(), name="add_product"),
    path("api/", include(router.urls), name="product_api"),
]
