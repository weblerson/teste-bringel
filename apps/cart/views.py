from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from django.db import transaction

from .serializers import CartRequestSerializer, CartSerializer, SaleRequestSerializer, SaleSerializer
from .models import Cart, Sale

from products.models import Product, PriceHistory


class CartViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):

    queryset = Cart.objects.all()
    permission_classes = [permissions.AllowAny]

    def create(self, request: Request, *args, **kwargs):
        customer_id = request.data.get('customer')
        product_id = request.data.get('product')

        if request.user.id != customer_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        cart: Cart = Cart.objects.get(customer__pk=customer_id)
        product: Product = Product.objects.get(pk=product_id)

        cart.product.add(product)
        cart.save()

        return Response(status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        match self.action:
            case 'retrieve':
                return CartSerializer

            case 'create':
                return CartRequestSerializer


class SaleViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):

    queryset = Sale.objects.all()
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def __get_product_price(product_id: int):
        price_history: PriceHistory = (PriceHistory.objects
                                       .filter(product__pk=product_id)
                                       .order_by('-start')
                                       .first())

        return price_history.price

    def list(self, request: Request, *args, **kwargs):
        instance: Sale = self.get_object()
        if request.user.id != instance.customer.id:
            if not request.user.is_staff:
                return Response(status=status.HTTP_403_FORBIDDEN)

            pass

        return super().list(request, *args, **kwargs)

    def retrieve(self, request: Request, *args, **kwargs):
        instance: Sale = self.get_object()
        if request.user.id != instance.customer.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        if request.user.id != request.data.get('customer'):
            return Response(status=status.HTTP_403_FORBIDDEN)

        customer_id = request.data.get('customer')
        delivery_address = request.data.get('delivery_address'),
        payment_method = request.data.get('payment_method')

        customer_cart: Cart = Cart.objects.get(customer__pk=customer_id)

        products = []
        for pk in request.data.getlist('products'):
            product: Product = Product.objects.get(pk=pk)
            if product not in customer_cart.product.all():
                return Response(status=status.HTTP_403_FORBIDDEN)

            customer_cart.product.remove(product)
            products.append(product)

        customer_cart.save()

        total = sum(self.__get_product_price(product.id) for product in products)

        sale: Sale = Sale.objects.create(
            customer=customer_cart.customer,
            total=total,
            delivery_address=delivery_address,
            payment_method=payment_method
        )
        for product in products:
            sale.products.add(product)

        return Response(status=status.HTTP_200_OK)

    def get_serializer_class(self):
        match self.action:
            case 'list' | 'retrieve':
                return SaleSerializer

            case 'create':
                return SaleRequestSerializer
