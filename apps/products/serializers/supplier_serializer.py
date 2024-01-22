from rest_framework import serializers

from ..tasks import update_product_sku

from ..models import Supplier


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ['id', 'name', 'address', 'phone']

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            update_product_sku.delay(instance.id)

        return super().update(instance, validated_data)
