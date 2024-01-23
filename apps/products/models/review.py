from django.db import models

from django.utils.translation import gettext as _

from authentication.models import Customer


class Review(models.Model):

    class Meta:
        ordering = ['product']

    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    value = models.FloatField()

    def __str__(self) -> str:
        return _(f'{self.customer.username} to {self.product.name}')
