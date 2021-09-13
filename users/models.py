"""
Models for the users app.
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

# pylint: disable = no-member


class TimeStamp(models.Model):
    """
    TimeStamp model to check when the object was created and modified
    """

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Defines the metadata of the class
        """

        abstract = True


class User(AbstractBaseUser, PermissionsMixin, TimeStamp):
    """
    Customized user model for E-commerce app
    """

    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        default=False, help_text="Is this user a staff member", blank=False, null=False
    )
    is_active = models.BooleanField(
        default=True, help_text="Active/Inactive status of a user"
    )
    name = models.CharField(max_length=50, blank=False, null=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        """
        Override default __str__ method to return email
        Return:
            (str): Value containing formatted id, name and email
        """
        return ", ".join([str(self.id), self.name, self.email])
