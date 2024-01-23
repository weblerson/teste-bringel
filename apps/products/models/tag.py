from django.db import models

from django.utils.translation import gettext_lazy as _


class Tag(models.Model):

    class Meta:
        ordering = ['name']

    name = models.CharField(primary_key=True, max_length=16)
    product = models.ForeignKey('products.Product', on_delete=models.DO_NOTHING, blank=False)

    def __str__(self) -> str:
        return _(f'{self.name} in {self.product}')
