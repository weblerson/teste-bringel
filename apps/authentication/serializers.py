from rest_framework import serializers

from django.db import transaction, DatabaseError

from .models import Customer

from cart.models import Cart
from cart.serializers import CartSerializer


class CustomerSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, write_only=True)
    is_staff = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password', 'is_staff']

    @staticmethod
    @transaction.atomic
    def __create_cart_for_user(customer_id: int):
        data = {
            'customer': customer_id
        }
        serializer: CartSerializer = CartSerializer(data=data)
        if not serializer.is_valid():
            return None

        return serializer.save()

    @staticmethod
    def validate_password(value):
        if ' ' in value:
            raise serializers.ValidationError('Password must not have any whitespaces')

        return value

    def create(self, validated_data):
        customer: Customer = Customer.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            is_staff=validated_data.get('is_staff')
        )

        cart: Cart = self.__create_cart_for_user(customer_id=customer.id)
        if cart is None:
            raise DatabaseError()

        return customer
