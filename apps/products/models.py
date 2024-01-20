from django.db import models

from django.utils.translation import gettext_lazy as _

from authentication.models import Customer


class Product(models.Model):

    class Category(models.IntegerChoices):
        SCIENCE = 1, _('Science')
        FICTION = 2,  _('Fiction')
        JOURNALISM = 3, _('Journalism')
        DIDACTIC = 4, _('Didactic')

    name = models.CharField(max_length=32)
    description = models.TextField()
    sku = models.CharField(max_length=32)
    category = models.IntegerField(choices=Category)
    average_review = models.FloatField()

    customers = models.ManyToManyField(Customer, through='Review')


class PriceHistory(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    start = models.DateField(auto_now=True)
    end = models.DateField()


class Tag(models.Model):

    name = models.CharField(primary_key=True, max_length=16)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)


class Supplier(models.Model):

    name = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
    phone = models.CharField(max_length=11)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)


class Review(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    value = models.FloatField()
