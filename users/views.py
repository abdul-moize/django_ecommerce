"""
This module contains
"""
from django.contrib.auth import get_user_model

# pylint: disable= no-self-use, no-member
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdmin
from .serializers import UserSerializer

User = get_user_model()


class UserAuthenticationAPIView(APIView):
    """
    Authenticates a user and returns a token
    """

    def post(self, request):
        """
        This functions validates the credentials and logs a user in
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (Response): A json object containing message, code and token
        """
        try:
            email = request.POST["email"]
            password = request.POST["password"]
            user = get_object_or_404(User, email=email)
            if check_password(password, user.password):
                token = Token.objects.get_or_create(user=user)
                response = {
                    "message": "Logged in successfully.",
                    "status_code": status.HTTP_200_OK,
                    "token": token[0].key,
                    "email": user.email,
                    "name": user.name,
                }
            else:
                response = {
                    "message": "Wrong email or password.",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }
        except KeyError:
            response = {
                "message": "Invalid Request.",
                "status_code": status.HTTP_400_BAD_REQUEST,
            }
        except Http404:
            response = {
                "message": "There was an error processing your request.",
                "status_code": status.HTTP_400_BAD_REQUEST,
            }

        return Response(response)


class UserAPIView(APIView):
    """
    User Management API
    post to add user
    put to login user
    patch to update user
    delete to remove user
    """

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdmin]

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
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "User created successfully.",
                        "status_code": status.HTTP_201_CREATED,
                        "user_data": serializer.data,
                    }
                )
            return Response(
                {
                    "message": serializer.errors,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }
            )
        except ValidationError as validation_error:
            response["message"] = " ".join(validation_error)
            response["status_code"] = status.HTTP_400_BAD_REQUEST

        return Response(response)

    def patch(self, request):
        """
        This function updates data of existing user
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (Response): A json object containing message and code
        """
        if request.user.is_authenticated:
            try:
                serializer = UserSerializer(
                    request.user, data=request.data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "message": "Changes updated successfully",
                            "status_code": status.HTTP_200_OK,
                            "new_data": serializer.data,
                        }
                    )

                return Response(
                    {
                        "message": serializer.errors,
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "data": serializer.data,
                    }
                )
            except ValidationError as error:
                return Response(
                    {
                        "message": " ".join(error),
                        "status_code": status.HTTP_400_BAD_REQUEST,
                    }
                )
        return Response(
            {
                "message": "No token provided in headers.",
                "status_code": status.HTTP_400_BAD_REQUEST,
            }
        )

    def delete(self, request):
        """
        This function deletes a user from database
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (Response): A json object containing message and code
        """
        response = {}
        if request.user.is_authenticated and IsAdmin().has_permission(
            request, self.delete
        ):
            try:
                get_object_or_404(User, email=request.POST["email"]).delete()
                response["message"] = "User deleted successfully"
                response["status_code"] = status.HTTP_200_OK
            except KeyError as key_error:
                response["message"] = str(key_error)
                response["status_code"] = status.HTTP_400_BAD_REQUEST
        else:
            response["message"] = "You don't have permission to delete user"
            response["status_code"] = status.HTTP_403_FORBIDDEN

        return Response(response)
