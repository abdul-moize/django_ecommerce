"""
Converts Models into Json Objects
"""
from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes the model CustomUser
    """

    class Meta:
        """
        Tells the models about which fields of the model to include in parsed response/request json.
        """

        model = CustomUser
        fields = ["email", "name", "is_ative", "is_staff", "date_joined"]
