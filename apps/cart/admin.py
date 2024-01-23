from django.contrib import admin

from django.utils.translation import gettext as _

from . import models


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):

    class CartInlineAdmin(admin.TabularInline):
        model = models.Cart.product.through
        readonly_fields = ('product',)
        can_delete = False

    fieldsets = (
        (_('Cart Owner'), {'fields': ('customer',)}),
    )

    inlines = (CartInlineAdmin,)


@admin.register(models.Sale)
class SaleAdmin(admin.ModelAdmin):

    class SaleInlineAdmin(admin.TabularInline):
        model = models.Sale.products.through
        readonly_fields = ('product',)
        can_delete = False

    fieldsets = (
        (_('Payment Info'), {'fields': ('total', 'payment_method', 'date')}),
        (_('Customer Info'), {'fields': ('customer', 'delivery_address')})
    )

    readonly_fields = ('total', 'payment_method', 'date', 'customer')

    inlines = (SaleInlineAdmin,)
