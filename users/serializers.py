"""
Converts Models into Json Objects
"""
from .models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'is_ative', 'is_staff', 'date_joined']
