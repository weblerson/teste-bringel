from django.db import models


class PriceHistory(models.Model):

    class Meta:
        ordering = ['start']

    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, blank=False)
    price = models.IntegerField()
    start = models.DateField(auto_now=True)
    end = models.DateField(null=True)
