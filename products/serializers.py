"""
Contains Serializers for products app
"""
import os

from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the product model
    """

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        # pylint: disable=no-member
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        os.remove(instance.image.path)
        super().update(instance, validated_data)
        return instance

    class Meta:
        """
        Tells the models about which fields of the model to include in parsed response/request json.
        """

        model = Product
        fields = "__all__"
