"""
Settings for admin site
"""
# pylint: disable = no-member, protected-access
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultAdmin

from .models import User


class UserAdmin(DefaultAdmin):
    """
    This class modifies the default options of User model for admin site
    """

    model = User
    list_display = ["id", "email", "name", "is_staff", "created_on"]
    list_filter = (
        "email",
        "name",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "name", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email", "id", "name", "is_staff", "is_active")
    ordering = ("id",)


admin.site.register(User, UserAdmin)
