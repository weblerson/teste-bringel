from django.db import models
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError

from .supplier import Supplier
from .price_history import PriceHistory

from authentication.models import Customer


class Product(models.Model):

    class Meta:
        ordering = ['id']

    class Category(models.IntegerChoices):
        SCIENCE = 1, _('Science')
        FICTION = 2,  _('Fiction')
        JOURNALISM = 3, _('Journalism')
        DIDACTIC = 4, _('Didactic')

    name = models.CharField(max_length=32)
    description = models.TextField()
    sku = models.CharField(max_length=32)
    category = models.IntegerField(choices=Category)
    average_review = models.FloatField(default=0.0)

    customers = models.ManyToManyField(Customer, through='Review')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=False, null=True)

    def clean(self):
        if not PriceHistory.objects.filter(product=self).exists():
            raise ValidationError({
                'products': _('Each product must be associated with at least one price.')
            })

        return super().clean()

    def __str__(self) -> str:
        return _(f'{self.name} - {self.sku}')
