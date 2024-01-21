from django.db.models import Avg

from .serializers import ProductSerializer

from celery import shared_task


@shared_task
def update_product_average_review(product_id: int):

    from .models import Product, Review

    product: Product = Product.objects.get(pk=product_id)
    reviews = Review.objects.filter(product__pk=product_id)

    average_review = reviews.aggregate(Avg('value')).get('value__avg')

    serializer: ProductSerializer = ProductSerializer()
    serializer.update(product, {'average_review': average_review})

    return average_review
