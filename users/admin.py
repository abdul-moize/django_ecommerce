"""
Settings for admin site
"""
# pylint: disable = no-member, protected-access
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultAdmin

from .models import Role, User


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
    all_fields = [
        field.name
        for field in User._meta.get_fields()
        if not field.auto_created and field.name != "password"
    ]
    fieldsets = (
        (None, {"fields": all_fields}),
        (None, {"fields": []}),
    )
    readonly_fields = ["created_on", "updated_on", "last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": all_fields + ["password1", "password2"],
            },
        ),
    )
    search_fields = ("email", "id", "name", "is_staff", "is_active")
    ordering = ("id",)


admin.site.register(User, UserAdmin)
admin.site.register(Role)
