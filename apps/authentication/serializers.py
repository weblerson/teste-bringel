from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'username', 'email']

    def create(self, validated_data):
        customer = Customer.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )

        return customer
