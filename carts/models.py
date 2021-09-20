"""
Models for cart app
"""
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import AuditTimeStamp, Product
from users.models import User


class Cart(AuditTimeStamp):
    """
    Model class that represents Cart
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    total_bill = models.DecimalField(
        _("Total Payable"),
        max_digits=20,
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
        total = Decimal(0)
        for item in self.cart_items.all():
            total += item.get_total()
        self.total_bill = Decimal(total)
        self.save()

    def __str__(self):
        return f"{self.user.name}'s Cart"


class CartItem(AuditTimeStamp):
    """
    Model class that represents a CartItem
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(
        _("Product quantity to buy"), default=0, validators=(MinValueValidator(1),)
    )
    tax = Decimal(16 / 100)

    def get_total(self):
        """
        Calculates and returns the total price of cart item
        Returns:
            (Decimal): Value containing total price of the cart item
        """
        # pylint: disable=no-member
        total = self.product.price * Decimal(self.quantity)
        total += self.tax * total
        return total

    def __str__(self):
        """
        Override default __str__() method
        Returns:
             (str): Value containing Product name and quantity
        """
        # pylint: disable=no-member
        return f"{self.product.name}, {self.quantity} of {self.cart.user.name}'s cart"
