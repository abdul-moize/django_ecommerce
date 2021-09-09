"""
Settings for admin site
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultAdmin

# from .forms import CustomUserChangeForm, CustomUserCreationForm
# pylint: disable = no-member, protected-access
from .models import CustomUser


class UserAdmin(DefaultAdmin):
    """
    This class modifies the default options of User model for admin site
    """

    model = CustomUser
    all_fields = [field.name for field in CustomUser._meta.fields]
    all_fields.sort()
    list_display = all_fields
    list_filter = (
        "email",
        "name",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password", "name")}),
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
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, UserAdmin)
