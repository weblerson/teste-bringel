from django.db import models

from django.utils.translation import gettext_lazy as _


class PriceHistory(models.Model):

    class Meta:
        ordering = ['start']

    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, blank=False)
    price = models.IntegerField()
    start = models.DateField(auto_now=True)
    end = models.DateField(null=True)

    def __str__(self) -> str:
        if self.end is None:
            return _(f'Actual price of {self.product.name}')

        return _(f'Old price of {self.product.name}')
