"""
This module contains
"""
from django.contrib.auth import authenticate, get_user_model, login

# pylint: disable= no-self-use, no-member
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .contants import HOME_PAGE_URL, LOGIN, REGISTER
from .permissions import IsAdmin
from .serializers import UserSerializer

User = get_user_model()


class TemplateUserLogin(APIView):
    """
    Displays login page and allows user to login
    """

    def post(self, request):
        """
        Validates and logs a user in
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (render or redirect):   redirects to homepage on success
                                    otherwise renders the login page
        """
        context = {}
        try:
            user = authenticate(
                request,
                username=request.POST["email"],
                password=request.POST["password"],
            )
            if user:
                login(request, user)
                return redirect(HOME_PAGE_URL)
            context["error_message"] = "Invalid Credentials"
            return render(request, LOGIN, context)
        except KeyError:
            context["error_message"] = "There was an error logging in."
            return render(request, LOGIN, context)

    def get(self, request):
        """
        Renders template of login/register page
        Returns:
            (render): Value containing template data to display
        """
        if request.user.is_authenticated:
            return redirect(HOME_PAGE_URL)
        return render(request, LOGIN, {})


class TemplateRegisterUser(APIView):
    """
    Adds a new user to database
    """

    def post(self, request):
        """
        Creates a new user and redirect to login page
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (render): Value containing template data to display
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {"msg": "Registration Successful. Please log in now."}
            return render(request, LOGIN, context)
        errors = serializer.errors
        context = {}
        if "email" in errors:
            context["email_error"] = ". ".join(errors["email"])
        if "name" in errors:
            context["name_error"] = ". ".join(errors["name"])
        if "password" in errors:
            context["password_error"] = errors["password"]
        context["register"] = True
        return render(request, REGISTER, context)


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
