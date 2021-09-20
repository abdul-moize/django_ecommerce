"""
Views for carts app
"""
# pylint: disable= no-self-use, no-member
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import Cart, CartItem, CartItemSerializer, CartSerializer


class CartsAPIView(APIView):
    """
    Carts APIView allows a user to add to cart, update a cart item, remove a cart item,
    view all or one cart item and clear all the cart items
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Adds a cart_item to cart
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (Response): Value containing information about operation status
        """
        user = request.user
        try:
            cart = get_object_or_404(Cart, user=user)
        except Http404:
            cart_serializer = CartSerializer(data={"user": user.id})
            if cart_serializer.is_valid():
                cart = cart_serializer.save(created_by=user)
            else:
                return Response(
                    {
                        "message": "There was a problem adding product to cart",
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "errors": cart_serializer.errors,
                    }
                )
        data = request.data.copy()
        data["cart"] = cart.id
        data["created_by"] = user.id
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=user)
            cart.update_bill()
            return Response(
                {
                    "message": "Product added to cart successfuly",
                    "Cart details": CartSerializer(cart).data,
                    "CartItems": CartItemSerializer(
                        CartItem.objects.filter(cart=cart), many=True
                    ).data,
                    "status_code": status.HTTP_200_OK,
                }
            )

        return Response(
            {
                "message": "There was a problem adding to cart",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": cart_serializer.errors,
            }
        )

    def get(self, request, item_pk=None):
        """
        Returns all the cart_items or one cart_item in the cart
        Args:
            request(HttpRequest): Value containing request data
            item_pk(int): Value containing primary key of a cart_item
        Returns:
            (Response): Value containing information about operation status
        """
        message = "Cart is empty"
        try:
            cart = get_object_or_404(Cart, user=request.user)
            if item_pk:
                message = "This item does not exist"
                cart_item = get_object_or_404(CartItem, pk=item_pk)
                return Response(
                    {
                        "message": "Item retrieved successfully.",
                        "item": CartItemSerializer(cart_item).data,
                        "status_code": status.HTTP_200_OK,
                    }
                )
            cart.update_bill()
            return Response(
                {
                    "message": "Items retrieved successfully.",
                    "cart_details": CartSerializer(cart).data,
                    "cart_items": CartItemSerializer(
                        cart.cart_items.all(), many=True
                    ).data,
                    "status_code": status.HTTP_200_OK,
                }
            )
        except Http404:
            return Response(
                {
                    "message": f"{message}. Please add items to cart first.",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }
            )

    def put(self, request, item_pk):
        """
        Updates a cart_item in cart
        Args:
            request(HttpRequest): Value containing request data
            item_pk(int): Value containing primary key of a cart_item
        Returns:
            (Response): Value containing information about operation status
        """
        try:
            cart = get_object_or_404(Cart, user=request.user)
            data = request.data.copy()
            data["cart"] = cart.id
            cart_item = get_object_or_404(CartItem, pk=item_pk)
            cart_item_serializer = CartItemSerializer(cart_item, data=data)
            if cart_item_serializer.is_valid():
                cart_item_serializer.save()
                return Response(
                    {
                        "message": "Product updated successfully",
                        "new_data": cart_item_serializer.data,
                        "status_code": status.HTTP_400_BAD_REQUEST,
                    }
                )
            return Response(
                {
                    "message": "There was a problem in updating the cart item.",
                    "errors": cart_item_serializer.errors,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }
            )

        except Http404:
            return Response(
                {
                    "message": "This item does not exist in cart. "
                    "Please add the item to cart first.",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }
            )

    def delete(self, request, item_pk=None):
        """
        Delete a cart_item or all items from cart
        Args:
            request(HttpRequest): Value containing request data
            item_pk(int): Value containing primary key of a cart_item
        Returns:
            (Response): Value containing information about operation status
        """
        try:
            cart = get_object_or_404(Cart, user=request.user)
            if item_pk:
                data = request.data.copy()
                data["cart"] = cart.id
                cart_item = get_object_or_404(CartItem, pk=item_pk)
                cart_item.delete()
                return Response(
                    {
                        "message": "Item deleted successfully",
                        "status_code": status.HTTP_200_OK,
                    }
                )
            for item in cart.cart_items.all():
                item.delete()
            return Response(
                {
                    "message": "Cart emptied successfully",
                    "status_code": status.HTTP_200_OK,
                }
            )
        except Http404:
            return Response(
                {
                    "message": "This item does not exist in cart. "
                    "Please add the item to cart first.",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }
            )
