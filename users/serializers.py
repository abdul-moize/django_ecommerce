"""
Converts Models into Json Objects
"""
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes the model CustomUser
    """

    class Meta:
        """
        Tells the models about which fields of the model to include in parsed response/request json.
        """

        model = User
        fields = ["email", "name", "is_ative", "is_staff", "date_joined"]
