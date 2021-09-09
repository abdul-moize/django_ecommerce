"""
Holds the forms through which data will be added to db
"""
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Modifies default user creation form
    """

    class Meta:
        """
        Defines which model and fields to include in the form
        """

        model = User
        fields = ("email", "name")


class CustomUserChangeForm(UserChangeForm):
    """
    Modifies default user data change form
    """

    class Meta:
        """
        Defines which model and fields to include in the form
        """

        model = User
        fields = ("password",)
