"""
Admin settings for carts app
"""
from django.contrib import admin

from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    """
    Cart model admin
    """

    list_display = ["id", "user"]
    list_filter = ["id", "user"]
    search_fields = ["id", "user"]
    ordering = ["id"]
    readonly_fields = [
        "created_on",
        "updated_on",
        "created_by",
        "all_cart_items",
        "total_bill",
    ]
    # pylint: disable=no-self-use

    def all_cart_items(self, obj):
        """
        Returns all cart_items associated with cart obj
        Args:
            obj(Cart): Cart instance
        Returns:
            (list): List containing product names of cart_items
        """
        return [item.product.name for item in obj.cart_items.all()]

    def save_model(self, request, obj, form, change):
        if obj.id is None:
            obj.created_by = request.user
        obj.save()


class CartItemAdmin(admin.ModelAdmin):
    """
    CartItem model admin
    """

    list_display = ["id", "product", "cart"]
    list_filter = ["id", "product", "cart"]
    search_fields = ["id", "product", "cart"]
    ordering = ["id"]
    readonly_fields = ["created_on", "updated_on", "created_by"]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
