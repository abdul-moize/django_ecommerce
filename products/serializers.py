"""
Contains Serializers for products app
"""
from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the product model
    """

    class Meta:
        """
        Tells the models about which fields of the model to include in parsed response/request json.
        """

        model = Product
        fields = "__all__"
