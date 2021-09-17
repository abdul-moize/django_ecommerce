"""
Models for the products app
"""
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import TimeStamp, User


class AuditTimeStamp(TimeStamp):
    """
    TimeStamp model for product class
    """

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, editable=False
    )

    class Meta:
        """
        Defines the metadata of the class
        """

        abstract = True


class Product(AuditTimeStamp):
    """
    Product model
    """

    objects = models.Manager()
    price = models.DecimalField(
        _("Product Price"),
        decimal_places=2,
        help_text="Price is in PKR/Rs",
        validators=[MinValueValidator(1)],
        max_digits=10,
    )
    stock_quantity = models.PositiveIntegerField(_("Product Quantity"))
    description = models.CharField(
        _("Product Description"), max_length=1000, blank=True
    )
    name = models.CharField(_("Product Name"), max_length=100)

    def __str__(self):
        """
        String representation of Product field
        Returns:
            (str): Value containing product name
        """
        return str(self.name)
