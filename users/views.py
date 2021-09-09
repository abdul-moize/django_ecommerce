"""
This module contains
"""
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User

# pylint: disable= no-self-use, no-member


class LoginUser(APIView):
    """
    This api request logs a user in and returns a token
    """

    def post(self, request):
        """
        This functions validates the credentials and logs a user in
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (Response): A json object containing message, code and token
        """
        response = {
            "message": "Wrong email or password",
            "code": status.HTTP_400_BAD_REQUEST,
        }
        try:
            email = request.POST["email"]
            password = request.POST["password"]
            user = get_object_or_404(User, email=email)
            if check_password(password, user.password):
                response["message"] = "Logged in successfully"
                response["code"] = status.HTTP_200_OK
                if not Token.objects.filter(user=user).exists():
                    token = Token.objects.create(user=user)
                else:
                    token = Token.objects.get(user=user)
                response["token"] = token.key
        except KeyError:
            response["message"] = "Bad Request"
        except Http404:
            response["message"] = "User does not exist"

        return Response(response)


class AddUser(APIView):
    """
    This is a post request to add a user to db
    """

    def post(self, request):
        """
        This function adds a user to db
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (Response): A json object containing message and code
        """
        response = {}
        try:
            name = request.POST["name"]
            email = request.POST["email"]
            password = request.POST["password"]
            validate_password(password)
            password = make_password(password)
            validate_email(email)
            user = User(name=name, email=email, password=password)
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


class UpdateUser(APIView):
    """
    Put request to update data of a user
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        This function updates data of existing user
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (Response): A json object containing message and code
        """
        try:
            user = request.user
            if "name" in request.POST:
                user.name = request.POST["name"]
            if "password" in request.POST:
                validate_password(request.POST["password"])
                user.password = make_password(request.POST["password"])
            user.save()
            return Response(
                {"message": "Changes updated successfully", "code": status.HTTP_200_OK}
            )
        except ValidationError as error:
            return Response(
                {"message": " ".join(error), "code": status.HTTP_400_BAD_REQUEST}
            )


class DeleteUser(APIView):
    """
    Put request to delete a user from database
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        This function deletes a user from database
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (Response): A json object containing message and code
        """
        user = request.user
        response = {}
        if user.is_superuser:
            try:
                get_object_or_404(User, email=request.POST["email"]).delete()
                response["message"] = "User deleted successfully"
                response["code"] = status.HTTP_200_OK
            except Http404:
                response["message"] = "No user exists with given email"
                response["code"] = status.HTTP_400_BAD_REQUEST
            except KeyError:
                response["message"] = "No email provided"
                response["code"] = status.HTTP_400_BAD_REQUEST
        else:
            response["message"] = "You don't have permission to delete user"
            response["code"] = status.HTTP_403_FORBIDDEN

        return Response(response)
