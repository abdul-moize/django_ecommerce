"""
Contains custom permissions
"""
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    User must be super user or staff member to access the view
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_staff and request.user.is_superuser
        )
