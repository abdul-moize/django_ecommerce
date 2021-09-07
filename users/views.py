from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.http import HttpResponse
from django.db.utils import IntegrityError
from rest_framework.views import APIView
import re
from .models import CustomUser
# Create your views here.


def index(request):
    return HttpResponse('worked')


class AddUser(APIView):

    def post(self, request):
        response_message = ''

        try:
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            if validate_password(password=password) and validate_email(email=email):
                user = CustomUser(name=name, email=email, password=password)
                validate_password(password)
                user.save()
                response_message = 'successfully created user'
        except KeyError:
            response_message = 'Error. Try again'
        except IntegrityError:
            response_message = 'Email already exists'

        return HttpResponse(response_message)

