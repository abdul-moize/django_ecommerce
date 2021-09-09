"""
Holds database models
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# pylint: disable = no-member


class TimeStamp(models.Model):
    """
    TimeStamp model to check when the object was created and modified
    """

    created_on = models.DateTimeField(default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Tells that this class is abstract
        """

        abstract = True


class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStamp):
    """
    Custom user model
    """

    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=50, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    def __str__(self):
        """
        Override default __str__ method to return email
        Return:
            (str): Value containing formatted id, name and email
        """
        return ", ".join([self.id, self.name, self.email])
