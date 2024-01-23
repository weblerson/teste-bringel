from rest_framework import serializers

from . import models
from products.models import Product


class CartRequestSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = models.Cart
        fields = ['customer', 'product']


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cart
        fields = ['id', 'customer', 'product']


class SaleRequestSerializer(serializers.ModelSerializer):

    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = models.Sale
        fields = ['customer', 'products', 'delivery_address', 'payment_method']


class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sale
        fields = ['id', 'customer', 'products', 'total', 'delivery_address', 'payment_method', 'date']
