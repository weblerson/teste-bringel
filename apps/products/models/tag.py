from django.db import models


class Tag(models.Model):

    name = models.CharField(primary_key=True, max_length=16)
    product = models.ForeignKey('products.Product', on_delete=models.DO_NOTHING, blank=False)
