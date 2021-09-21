"""
Admin settings for carts app
"""
from django.contrib import admin

from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    """
    Admin representation of Cart model
    """

    list_display = [
        "id",
        "user",
        "created_on",
        "updated_on",
        "created_by",
        "total_bill",
    ]
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
        obj.save(created_by=request.user)


class CartItemAdmin(admin.ModelAdmin):
    """
    Admin representation of CartItem model
    """

    list_display = ["id", "product", "cart", "created_on", "updated_on", "created_by"]
    list_filter = ["id", "product", "cart"]
    search_fields = ["id", "product", "cart"]
    ordering = ["id"]
    readonly_fields = ["created_on", "updated_on", "created_by"]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
