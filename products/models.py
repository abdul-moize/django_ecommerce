"""
Models for the products app
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class TimeStamp(models.Model):
    """
    TimeStamp model for product class
    """

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """
        Defines the metadata of the class
        """

        abstract = True


class Product(TimeStamp):
    """
    Product model
    """

    price = models.IntegerField(_("Product Price"))
    quantity = models.IntegerField(_("Product Quantity"))
    description = models.CharField(
        _("Product Description"), max_length=1000, blank=True
    )
    # image = models.ImageField(_("Product Image"))
    price_unit = models.CharField(_("Currency"), max_length=3)
    name = models.CharField(_("Product Name"), max_length=100)

    def __str__(self):
        """
        Overrides default __str__()
        Returns:
            (str): Value containing product name
        """
        return str(self.name)
