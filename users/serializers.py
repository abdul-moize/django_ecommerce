"""
Converts Models into Json Objects
"""
# pylint: disable= no-self-use
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model
    """

    def create(self, validated_data):
        """
        Creates objects of User model
        Args:
            validated_data(dict):
        Returns:
            (User model object): Model containing User data
        """
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates the data of instance with validated_data
        Args:
            instance(models.Model):
            validated_data(dict):
        Returns:
            (models.Model):
        """
        if "name" in validated_data:
            instance.name = validated_data["name"]
        if "email" in validated_data:
            instance.email = validated_data["email"]
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance

    def validate_email(self, value):
        """
        Validates the field email of User model
        Args:
            value(str): Value containing email
        Returns:
            (str): Validated email
        """
        return value.lower()

    def validate_password(self, value):
        """
        Validates the field password of User model
        Args:
            value(str): Value containg password
        Returns:
            (str): Validated password
        """
        validate_password(value)
        return value

    class Meta:
        """
        Tells the models about which fields of the model to include in parsed response/request json.
        """

        model = User
        fields = ["email", "name", "password"]
