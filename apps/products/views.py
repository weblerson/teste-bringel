from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import mixins
from rest_framework.decorators import action

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Supplier, Tag, PriceHistory, Review
from .serializers import (ProductSerializer,
                          SupplierSerializer,
                          TagSerializer,
                          PriceHistorySerializer,
                          ReviewSerializer)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case 'list' | 'retrieve':
                permission_classes = [permissions.AllowAny]

            case _:
                permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case 'list' | 'retrieve':
                permission_classes = [permissions.AllowAny]

            case _:
                permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]


class TagViewSet(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case 'list':
                permission_classes = [permissions.AllowAny]

            case 'destroy':
                permission_classes = [permissions.IsAdminUser]

            case _:
                permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]


class PriceHistoryViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):

    queryset = PriceHistory.objects.all()
    serializer_class = PriceHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case 'list' | 'retrieve':
                permission_classes = [permissions.AllowAny]

            case _:
                permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]


class ReviewViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case 'list' | 'retrieve':
                permission_classes = [permissions.AllowAny]

            case _:
                permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]


class RecommendationAlgorithmViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer

    @action(detail=True, url_path='')
    def list_related_products(self, request: Request, pk=None):
        """
        List all products that have the same category
        """

        main_product: Product = Product.objects.get(pk=pk)
        related_products = Product.objects.filter(category=main_product.category).exclude(pk=main_product.id)

        serializer: ProductSerializer = ProductSerializer(related_products, many=True)

        return Response({
            'products': serializer.data,
        }, status=status.HTTP_200_OK)
