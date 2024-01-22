from django.db.models import Avg

from celery import shared_task

from .utils import SkuUtils


@shared_task(max_retries=3)
def update_product_average_review(product_id: int):

    from .models import Product, Review
    from .serializers import ProductSerializer

    product: Product = Product.objects.get(pk=product_id)
    reviews = Review.objects.filter(product__pk=product_id)

    average_review = reviews.aggregate(Avg('value')).get('value__avg')

    serializer: ProductSerializer = ProductSerializer()
    serializer.update(product, {'average_review': average_review})

    return True


@shared_task(max_retries=3)
def update_product_sku(product_id=None, supplier_id=None):

    from .models import Product, Supplier

    if product_id is not None:
        product: Product = Product.objects.get(pk=product_id)
        sku = SkuUtils.generate_sku(product.supplier.name, product.name, product.category)

        product.sku = sku
        product.save()

    if supplier_id is not None:
        supplier: Supplier = Supplier.objects.get(pk=supplier_id)
        product: Product = Product.objects.get(supplier=supplier)
        sku = SkuUtils.generate_sku(product.supplier.name, product.name, product.category)

        product.sku = sku
        product.save()

    return True
