"""
Models for cart app
"""
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from carts.constants import CART_STATUS, OPEN
from products.models import AuditTimeStamp, Product
from users.models import User


class Cart(AuditTimeStamp):
    """
    Model class that represents Cart
    """

    status = models.CharField(max_length=40, choices=CART_STATUS, default=OPEN)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="cart")
    total_bill = models.DecimalField(
        _("Total Payable"),
        max_digits=10,
        validators=(MinValueValidator(1),),
        decimal_places=2,
        default=Decimal(0),
    )

    def update_bill(self):
        """
        Updates the bill by traversing all the cart items
        Returns:
            None
        """
        # pylint: disable=no-member
        self.total_bill = self.cart_items.aggregate(total=Sum("item_total"))["total"]
        if self.total_bill is None:
            self.total_bill = 0
        self.save()

    def __str__(self):
        return f"{self.user.name}'s Cart"


class CartItem(AuditTimeStamp):
    """
    Model class that represents a CartItem
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="+")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(
        _("Product quantity to buy"), default=1, validators=(MinValueValidator(1),)
    )
    item_total = models.PositiveIntegerField(
        _("Total price of Cart Item"), validators=(MinValueValidator(1),), null=True
    )

    def delete(self, *args, **kwargs):
        """
        Updates bill whenever an item is deleted
        Args:
            args(list): List containing arguments
            kwargs(dict): Dictionary containing key value arguments
        Returns:
            None
        """
        # pylint: disable=no-member
        self.product.stock_quantity += self.quantity
        self.product.save()
        cart = self.cart
        super().delete(*args, **kwargs)
        cart.update_bill()

    def save(self, *args, **kwargs):
        """
        Updates bill whenever an item is updated
        Args:
            args(list): list containing different arguments
            kwargs(dict): dictionary containing different key value arguments
        Returns:
            None
        """
        # pylint: disable=no-member
        self.item_total = Decimal(self.quantity) * self.product.price
        super().save(*args, **kwargs)
        self.cart.update_bill()

    def __str__(self):
        """
        Override default __str__() method
        Returns:
             (str): Value containing Product name and quantity
        """
        # pylint: disable=no-member
        return f"{self.product.name}, {self.quantity} of {self.cart.user.name}'s cart"
