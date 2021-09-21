"""
Carts app settings
"""
from django.apps import AppConfig


class CartsConfig(AppConfig):
    """
    Carts app default configurations
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "carts"
