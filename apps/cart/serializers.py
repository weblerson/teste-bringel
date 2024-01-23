from rest_framework import serializers

from . import models


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cart
        fields = ['id', 'customer', 'products']


class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sale
        fields = ['id', 'customer', 'products', 'total', 'delivery_address', 'payment_method', 'date']
