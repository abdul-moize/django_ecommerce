"""
Contains custom permissions for products app
"""
from rest_framework.permissions import BasePermission

from users.contants import CONTENT_MANAGER


class IsContentManager(BasePermission):
    """
    Tells if user can create or update products
    """

    def has_permission(self, request, view):
        """
        True to grant permission
        False to deny permission
        Args:
            request():
            view():
        Returns:
            (bool):
        """
        if request.user.is_superuser or request.user.is_staff:
            return True
        if request.user.role.code == CONTENT_MANAGER:
            return True
        return False
