"""
App settings
"""
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Product app settings
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "products"
