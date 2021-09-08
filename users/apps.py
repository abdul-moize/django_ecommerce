"""
Contains app settings
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Defines app name and other settings
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
