from rest_framework import serializers

from django.utils import timezone

from ..models import PriceHistory, Product


class PriceHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PriceHistory
        fields = ['id', 'product', 'price', 'start', 'end']

    def create(self, validated_data):
        product: Product = validated_data.get('product')

        price_history = PriceHistory.objects.filter(product=product).order_by('start')
        if price_history.exists():
            last: PriceHistory = price_history.last()
            last.end = timezone.now()
            last.save()

        return super().create(validated_data)
