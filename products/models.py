"""
Models for the products app
"""
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from products.constants import IMAGES_PATH
from users.models import TimeStamp, User


def image_path(instance, filename):
    """
    Returns the path to store the image file at
    Args:
        instance(Product): Value containing product data
        filename(str): Value containing image filename
    Returns:
        (str): Value containing location to store file
    """
    return f"{IMAGES_PATH}{instance.name}_{filename}"


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

    image = models.ImageField(upload_to=image_path, default="default_image.png")
    name = models.CharField(_("Product Name"), max_length=100)

    def get_price(self):
        """
        Returns price with currency
        Returns:
            (str): Value containing price and currency
        """
        return f"Rs. {self.price}"

    def save(self, *args, **kwargs):
        # pylint: disable=no-member
        if self.id is not None:
            product = Product.objects.get(id=self.id)
            if product.image.name != "default_image.png":
                product.image.delete(False)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # pylint: disable=no-member
        if self.image.name != "default_image.png":
            self.image.delete(False)
        super().delete(*args, **kwargs)

    def __str__(self):
        """
        String representation of Product field
        Returns:
            (str): Value containing product name
        """
        return str(self.name)
