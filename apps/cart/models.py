from django.db import models

from django.utils.translation import gettext_lazy as _

from authentication.models import Customer
from products.models import Product


class Cart(models.Model):

    class Meta:
        ordering = ['id']

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self) -> str:
        return _(f'Cart of {self.customer.username}')


class Sale(models.Model):

    class Meta:
        ordering = ['id']

    class Payment(models.IntegerChoices):
        PIX = 1, _('Pix'),
        CREDIT = 2, _('Credit')
        DEBIT = 3, _('Debit')

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(Product)

    total = models.IntegerField()
    delivery_address = models.CharField(max_length=64)
    payment_method = models.IntegerField(choices=Payment)
    date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f'Sold to {self.customer.username} at {self.date}'
