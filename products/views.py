"""
Contains Views for products app
"""
# pylint: disable=no-self-use, no-member
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product
from .permissions import IsContentManager
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ViewSet):
    """
    Product viewset
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
        actions = ["create", "update", "delete"]
        if self.action in actions:
            permission_classes = [IsAuthenticated, IsContentManager]

        return [permission() for permission in permission_classes]

    def create(self, request):
        """
        Creates new Products
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (dict): Value containing product data
        """
        data = request.data.dict()
        data["created_by"] = request.user.id
        print(data)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Product created successfully",
                    "product_data": serializer.data,
                    "status_code": status.HTTP_201_CREATED,
                }
            )
        return Response(
            {
                "message": "Bad request",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors,
            }
        )

    def list(self, request):
        """
        Returns all products
        Args:
            request(HttpRequest): Value containing request data
        Returns:
            (dict): Value containing all products
        """
        if request.method == "GET":
            queryset = Product.objects.all()
            if queryset:
                return Response(
                    {
                        "products": ProductSerializer(queryset, many=True).data,
                        "status_code": status.HTTP_200_OK,
                    }
                )
            return Response(
                {
                    "message": "No products found",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }
            )
        return Response(
            {"message": "Bad request", "status_code": status.HTTP_400_BAD_REQUEST}
        )

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific product
        Args:
            request(HttpRequest): Value containing request data
            pk(int): id(primary_key) of Product
        Returns:
            (dict): Value containing a specific product
        """
        if request.method == "GET":
            product = get_object_or_404(Product, pk=pk)
            return Response(
                {
                    "product": ProductSerializer(product).data,
                    "status_code": status.HTTP_200_OK,
                }
            )
        return Response(
            {"message": "Bad request", "status_code": status.HTTP_400_BAD_REQUEST}
        )

    def update(self, request, pk=None):
        """
        Updates an existing product
        Args:
            request(HttpRequest): Value containing request data
            pk(int): id(primary_key) of Product
        Returns:
            (dict): Value containing new/updated product data
        """
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "messagae": "Changes updated successfully",
                    "status_code": status.HTTP_200_OK,
                    "updated_data": serializer.data,
                }
            )
        return Response(
            {
                "message": "Bad Request",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors,
            }
        )

    def destroy(self, request, pk=None):
        """
        Deletes a product from database
        Args:
            request(HttpRequest): Value containing Request data
            pk(int): id(primary key) of product
        Returns:
            (dict): Value containing delete operation status
        """
        if request.method == "DELETE":
            get_object_or_404(Product, pk=pk).delete()
            return Response(
                {
                    "message": "Product deleted successfully",
                    "status_code": status.HTTP_200_OK,
                }
            )
        return Response(
            {"message": "Bad request", "status_code": status.HTTP_400_BAD_REQUEST}
        )
