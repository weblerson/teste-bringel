from django.db import models

from django.utils.translation import gettext_lazy as _


class Supplier(models.Model):

    class Meta:
        ordering = ['id']

    name = models.CharField(max_length=32, unique=True)
    address = models.CharField(max_length=64)
    phone = models.CharField(max_length=11, unique=True)

    def __str__(self) -> str:
        return _(f'{self.name}')
