"""
Serializers for carts models
"""
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from carts.models import Cart, CartItem
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """
    CartItem model serializer
    """

    product_data = serializers.SerializerMethodField()
    # pylint: disable=no-self-use

    def get_product_data(self, obj):
        """
        Returns serialized data of product
        Args:
            obj(Cart Item):  Value containing cart item data
        Returns:
            (dict): Value containing product data
        """
        return ProductSerializer(instance=obj.product).data

    def create(self, validated_data):
        """
        Creates a CartItem
        Args:
            validated_data(dict): Value containing verified data
        Returns:
            (CartItem): Value containing created CartItem instance
        """
        # pylint: disable=no-member
        cart = validated_data["cart"]
        filter_item = cart.cart_items.filter(product=validated_data["product"])
        if filter_item.exists():
            cart_item = filter_item.get()
            cart_item.quantity += validated_data["quantity"]
            if cart_item.quantity > cart_item.product.stock_quantity:
                raise serializers.ValidationError(
                    _("Product cannot be added because it's out of stock")
                )
        else:
            cart_item = CartItem.objects.create(**validated_data)
        cart_item.save()
        validated_data["cart"].update_bill()
        return cart_item

    def validate(self, attrs):
        if attrs["product"].stock_quantity < attrs["quantity"]:
            raise serializers.ValidationError(
                _("Product cannot be added because it's out of stock")
            )
        return attrs

    class Meta:
        """
        Tells model and fields to include in parsed/json object
        """

        model = CartItem
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    """
    Cart model serializer
    """

    cart_items = CartItemSerializer(many=True)

    class Meta:
        """
        Tells the fields to include in parsed/json object
        """

        # pylint: disable=protected-access, no-member
        model = Cart
        fields = "__all__"
