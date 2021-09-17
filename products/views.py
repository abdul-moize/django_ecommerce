"""
Contains Views for products app
"""
# pylint: disable=no-self-use, no-member
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product
from .permissions import IsContentManager
from .serializers import ProductSerializer


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
