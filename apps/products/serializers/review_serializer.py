from rest_framework import serializers

from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['product', 'customer', 'value']

    def create(self, validated_data):
        instance: Review = super().create(validated_data)

        from ..tasks import update_product_average_review
        update_product_average_review.delay(instance.product.id)

        return instance

    def update(self, instance: Review, validated_data):
        from ..tasks import update_product_average_review

        instance: Review = super().update(instance, validated_data)
        update_product_average_review.delay(instance.product.id)

        return instance
