"""
Contains Serializers for products app
"""
from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the product model
    """

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return Product.objects.create(**validated_data)

    class Meta:
        """
        Tells the models about which fields of the model to include in parsed response/request json.
        """

        model = Product
        fields = "__all__"
