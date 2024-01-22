from rest_framework import serializers

from ..tasks import update_product_sku

from ..models import Product

from ..utils import SkuUtils


class ProductSerializer(serializers.ModelSerializer):

    sku = serializers.CharField(max_length=32, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'sku', 'category', 'average_review', 'customers', 'supplier']

    def create(self, validated_data):
        supplier_name = validated_data.get('supplier').name
        product_name = validated_data.get('name')
        category = validated_data.get('category')

        sku = SkuUtils.generate_sku(supplier_name, product_name, category)

        product = Product.objects.create(
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            sku=sku,
            category=validated_data.get('category'),
            supplier=validated_data.get('supplier')
        )

        return product

    def update(self, instance, validated_data):
        if 'name' or 'category' in validated_data:
            update_product_sku.delay(instance.id)

        return super().update(instance, validated_data)
