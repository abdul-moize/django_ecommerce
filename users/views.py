"""
This module contains
"""
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser

# Create your views here.
# pylint: disable= no-self-use


class AddUser(APIView):
    """
    This is a post request to add a user to db
    """

    def post(self, request):
        """
        This function adds a user to db
        Args:
            request():
        Returns:
            (Response): a json object containing code and message
        """
        response = {}
        try:
            name = request.POST["name"]
            email = request.POST["email"]
            password = request.POST["password"]
            validate_password(password)
            password = make_password(password)
            validate_email(email)
            user = CustomUser(name=name, email=email, password=password)
            user.save()
            response["message"] = "successfully created user"
            response["code"] = status.HTTP_201_CREATED
        except KeyError:
            response["message"] = "Error. Try again"
            response["code"] = status.HTTP_400_BAD_REQUEST
        except IntegrityError:
            response["message"] = "Email already exists"
            response["code"] = status.HTTP_409_CONFLICT
        except ValidationError as error:
            response["message"] = " ".join(error)
            response["code"] = status.HTTP_400_BAD_REQUEST

        return Response(response)
