"""
Contains Views for products app
"""
# pylint: disable=no-self-use, no-member
from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.contants import CONTENT_MANAGER, ROLES, SYSTEM_ADMIN

from .constants import ADD_PRODUCT, HOMEPAGE, PRODUCT_PAGE
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
        context = {
            "products": Product.objects.all(),
            "content_managers": [ROLES[CONTENT_MANAGER], ROLES[SYSTEM_ADMIN]],
        }
        return render(request, HOMEPAGE, context)


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
        return render(request, PRODUCT_PAGE, context)


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
        return render(request, ADD_PRODUCT, {})

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
            return render(request, ADD_PRODUCT, context)

        errors = serializer.errors
        context = {
            "name_error": ", ".join(errors["name"]) if "name" in errors else None,
            "quantity_error": errors["stock_quantity"]
            if "stock_quantity" in errors
            else None,
            "price_error": errors["price"] if "price" in errors else None,
        }
        return render(request, ADD_PRODUCT, context)


class ProductViewSet(viewsets.ModelViewSet):
    # pylint: disable=too-many-ancestors
    """
    Product ModelViewSet
    """

    # pylint: disable =invalid-name
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = [TokenAuthentication]

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
