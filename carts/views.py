"""
Views for carts app
"""
# pylint: disable= no-self-use, no-member
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.contants import HOME_PAGE_URL

from .constants import OPEN, SUBMITTED
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
        cart = Cart.objects.get_or_create(user=user, status=OPEN, created_by=user)[0]
        data = request.data.copy()
        data["cart"] = cart.id
        data["created_by"] = user.id
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(
                {
                    "message": "Product added to cart successfuly",
                    "Cart details": CartSerializer(
                        Cart.objects.get(user=user, status=OPEN)
                    ).data,
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
                "errors": serializer.errors,
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
        try:
            carts = Cart.objects.filter(user=request.user)
            if item_pk:
                cart = get_object_or_404(Cart, user=request.user, pk=item_pk)
                return Response(
                    {
                        "message": "Item retrieved successfully.",
                        "cart_detail": CartSerializer(cart).data,
                        "items": CartItemSerializer(
                            cart.cart_items.all(), many=True
                        ).data,
                        "status_code": status.HTTP_200_OK,
                    }
                )
            return Response(
                {
                    "message": "Items retrieved successfully.",
                    "cart_details": CartSerializer(carts, many=True).data,
                    "status_code": status.HTTP_200_OK,
                }
            )
        except Http404:
            return Response(
                {
                    "message": "Such cart does not exist",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }
            )

    def patch(self, request):
        """
        Submits a cart
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (Response): Value containing operation status
        """
        if request.method != "PATCH":
            return Response(
                {
                    "message": "Only PATCH request is allowed",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }
            )
        try:

            cart = get_object_or_404(Cart, user=request.user, status=OPEN)
            if cart.cart_items:
                serializer = CartSerializer(
                    cart, data={"status": SUBMITTED}, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "message": "Order submitted successfully",
                            "status_code": status.HTTP_200_OK,
                        }
                    )
            return Response(
                {"message": "Cart is empty", "status_code": status.HTTP_400_BAD_REQUEST}
            )

        except Http404:
            return Response(
                {
                    "message": "Such cart does not exist",
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
            cart = get_object_or_404(Cart, user=request.user, status=OPEN)
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
            cart = get_object_or_404(Cart, user=request.user, status=OPEN)
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


class TemplateCartsAPIView(APIView):
    """
    Allow the user to view the cart and modify its contents
    """

    authentication_classes = [SessionAuthentication]

    def get(self, request):
        """
        Renders the template containing cart details
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (render): Value containing template data to display
        """
        if request.user.is_authenticated:
            try:
                context = {
                    "cart_items": get_object_or_404(
                        Cart, user=request.user, status=OPEN
                    ).cart_items.all()
                }
                return render(request, "cart_detail.html", context)
            except Http404:
                context = {
                    "error_message": "Your cart is empty. Please add products to cart."
                }
                return render(request, "cart_detail.html", context)
        context = {"error_message": "You are not logged in. Please Log in."}
        return render(request, "cart_detail.html", context)

    def post(self, request):
        """
        Allows the user to submit or change cart details
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (render): Value containing template data to display
        """
        if request.user.is_authenticated:
            context = {
                "cart_items": get_object_or_404(
                    Cart, user=request.user, status=OPEN
                ).cart_items.all()
            }
            cart = get_object_or_404(Cart, user=request.user, status=OPEN)
            old_cart_items = cart.cart_items.all()
            product_ids = request.POST.getlist("product")
            product_quantities = request.POST.getlist("quantity")

            for index, item in enumerate(old_cart_items):
                if int(item.product.id) == int(product_ids[index]):
                    item.quantity = int(product_quantities[index])
                    item.save()
                else:
                    item.delete()
            if request.POST["is_checkout"] == "true" and len(product_ids) > 0:
                cart.status = SUBMITTED
                cart.save()
                return redirect(HOME_PAGE_URL)
            return render(request, "cart_detail.html", context)
        context = {"error_message": "You are not logged in. Please log in."}
        return render(request, "cart_detail.html", context)


class TemplateViewCarts(APIView):
    """
    Allows the users to see his order history
    """

    authentication_classes = [SessionAuthentication]

    def get(self, request):
        """
        Renders a page containing previous orders of the user
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (render): Value containing template data to display
        """

        carts = Cart.objects.filter(~Q(status=OPEN), user=request.user)
        if carts.exists():
            context = {"carts": carts}
            return render(request, "orders.html", context)
        context = {"error_message": "You do not have any previous orders"}
        return render(request, "orders.html", context)
