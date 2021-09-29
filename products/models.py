"""
Models for the products app
"""
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from products.constants import DEFAULT_PRODUCT_IMAGE
from products.utils import image_path
from users.models import TimeStamp, User


class AuditTimeStamp(TimeStamp):
    """
    TimeStamp model to check when the object was created and modified
    """

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, editable=False, related_name="+"
    )

    def save(self, *args, **kwargs):
        """
        Populates the created_by fields
        Args:
            args(list): list containing different arguments
            kwargs(dict): dictionary containing different key value arguments
        Returns:
            None
        """
        # pylint: disable=no-member
        if "created_by" in kwargs and self.created_by is None and self.id is None:
            self.created_by = kwargs["created_by"]
        super().save(*args)

    class Meta:
        """
        Defines the metadata of the class
        """

        abstract = True


class Product(AuditTimeStamp):
    """
    Product model
    """

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

    image = models.ImageField(upload_to=image_path, null=True)
    name = models.CharField(_("Product Name"), max_length=100)

    def get_price(self):
        """
        Returns a formatted price with the currency of price
        Returns:
            (str): Value containing formatted price and symbol of currency
        """
        formatted_price = []
        price = list(str(self.price))
        decimal = price[-3:]
        price = price[0:-3]
        price.reverse()
        for index, value in enumerate(price):
            formatted_price += [value]
            if (index + 1) % 3 == 0 and index < len(price) - 1:
                formatted_price += [","]
        formatted_price.reverse()
        formatted_price += decimal
        return f"Rs. {''.join(formatted_price)}"

    def save(self, *args, **kwargs):
        # pylint: disable=no-member
        if self.id is not None and self.image:
            product = Product.objects.filter(id=self.id).first()
            if (
                product is not None
                and product.image.name != DEFAULT_PRODUCT_IMAGE
                and product.image.name != self.image.name
            ):
                product.image.delete(False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # pylint: disable=no-member
        if self.image and self.image.name != DEFAULT_PRODUCT_IMAGE:
            self.image.delete(False)
        super().delete(*args, **kwargs)

    def __str__(self):
        """
        String representation of Product field
        Returns:
            (str): Value containing product name
        """
        return str(self.name)
