from django.db import models


class Supplier(models.Model):

    name = models.CharField(max_length=32, unique=True)
    address = models.CharField(max_length=64)
    phone = models.CharField(max_length=11, unique=True)
