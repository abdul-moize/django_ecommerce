"""
Model forms for users app
"""
from django import forms

from users.models import User


class LoginForm(forms.ModelForm):
    """
    Login form for user
    """

    class Meta:
        """
        Defines the meta data of class
        """

        model = User
        fields = ["email", "password"]


class RegisterForm(forms.ModelForm):
    """
    Registeration Form for user
    """

    class Meta:
        """
        Defines the meta data of class
        """

        model = User
        fields = ["email", "password", "name"]
