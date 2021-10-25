"""
Contains Views for products app
"""
# pylint: disable=no-self-use, no-member
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.views import CartsAPIView

from .models import Product
from .permissions import IsContentManager
from .serializers import ProductSerializer


class ProductHomePageView(APIView):
    """
    Renders the homepage of products
    """

    authentication_classes = [SessionAuthentication]

    def get(self, request):
        """
        Renders the homepage template
        Args:
            request(HttpRequest):
        Returns:
            (render): Value containing template data to display
        """
        is_content_manager = False
        if IsContentManager().has_permission(request, None):
            is_content_manager = True
        context = {
            "products": Product.objects.filter(~Q(stock_quantity=0)).all(),
            "can_manage_content": is_content_manager,
        }
        return render(request, "homepage.html", context)


class ProductView(APIView):
    """
    Render details of a product
    """

    authentication_classes = [SessionAuthentication]

    def get(self, request, product_pk):
        """
        Displays a product
        Args:
            request(HttpRequest): Value containing request data
            product_pk(int): Value containing primary key of product to view
        Returns:
            (render):
        """
        context = {"product": get_object_or_404(Product, pk=product_pk)}
        return render(request, "product_page.html", context)

    def post(self, request, product_pk):
        """
        Adds a product to cart
        request(HttpRequest): Value containing request data
            product_pk(int): Value containing primary key of product to view
        Returns:
            (render): Value containing template data to display
        """
        response = CartsAPIView().post(request)
        if response.status_code == status.HTTP_200_OK:
            context = {
                "product": get_object_or_404(Product, pk=product_pk),
                "added_to_cart": "Product added to cart.",
            }
        else:
            context = {
                "product": get_object_or_404(Product, pk=product_pk),
                "message": "There was a problem adding to cart. Please try again.",
            }

        return render(request, "product_page.html", context)


class AddProductView(APIView):
    """
    Add a Product to database via template
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsContentManager, IsAuthenticated]

    def get(self, request):
        """
        Renders the add product template
        Args:
            request(HttpRequest):
        Returns:
            (render): Value containing template data to display
        """
        return render(request, "add_product.html", {})

    def post(self, request):
        """
        Adds a new product
        Args:
            request(HttpRequest):
        Returns:
            (render): Value containing template data to display
        """
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            context = {"message": "Product created Successfully"}
            return render(request, "add_product.html", context)

        errors = serializer.errors
        context = {
            "name_error": ", ".join(errors["name"]) if "name" in errors else None,
            "quantity_error": errors["stock_quantity"]
            if "stock_quantity" in errors
            else None,
            "price_error": errors["price"] if "price" in errors else None,
        }
        return render(request, "add_product.html", context)


class ProductViewSet(viewsets.ModelViewSet):
    # pylint: disable=too-many-ancestors
    """
    Product ModelViewSet
    """

    # pylint: disable =invalid-name
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_authenticators(self):
        authentication_classes = []
        if self.request.method != "GET":
            authentication_classes = [TokenAuthentication]
        return [authentication() for authentication in authentication_classes]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = []
        actions = ["create", "update", "destroy"]
        if self.action in actions:
            permission_classes = [IsAuthenticated, IsContentManager]

        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a product from database
        Args:
            request(HttpRequest): Value containing Request data
        Returns:
            (dict): Value containing delete operation status
        """
        if request.method == "DELETE":
            self.get_object().delete()
            return Response(
                {
                    "message": "Product deleted successfully",
                    "status_code": status.HTTP_200_OK,
                }
            )
        return Response(
            {
                "message": "There was a problem in deleting the product",
                "status_code": status.HTTP_400_BAD_REQUEST,
            }
        )
