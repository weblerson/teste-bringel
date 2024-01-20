from django.db import models

from authentication.models import Customer


class Review(models.Model):

    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    value = models.FloatField()
