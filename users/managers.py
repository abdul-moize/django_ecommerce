"""
Contains Managers for models
"""
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        validate_email(email.lower())
        validate_password(password)
        if extra_fields["name"] not in ["", " "]:
            email = email.lower()
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
        else:
            raise ValueError(_("Name can not be blank"))
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["is_active"] = True
        return self.create_user(email, password, **extra_fields)
