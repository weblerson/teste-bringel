from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import CartRequestSerializer, CartSerializer
from .models import Cart

from products.models import Product


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
