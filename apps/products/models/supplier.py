from django.db import models


class Supplier(models.Model):

    class Meta:
        ordering = ['id']

    name = models.CharField(max_length=32, unique=True)
    address = models.CharField(max_length=64)
    phone = models.CharField(max_length=11, unique=True)
