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
        Checks if the user has a specific permission or not
        Args:
            request(HttpRequest): Value containing request data
            view(HttpView): Value containing view data
        Returns:
            (bool): True is a user has permission otherwise False.
        """
        return (
            request.user.is_superuser
            or request.user.is_staff
            or request.user.role.code == CONTENT_MANAGER
        )
