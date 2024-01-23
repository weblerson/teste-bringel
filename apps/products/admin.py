from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    class CustomerInlineAdmin(admin.TabularInline):
        model = models.Product.customers.through
        readonly_fields = ('customer', 'product', 'value')
        can_delete = False

    fieldsets = (
        (_('Product Info'), {'fields': ('name', 'description', 'sku', 'category', 'average_review')}),
        (_('Supplier'), {'fields': ('supplier',)}),
    )

    readonly_fields = ('sku', 'average_review')

    inlines = (CustomerInlineAdmin,)


@admin.register(models.Supplier)
class SupplierAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('Supplier Info'), {'fields': ('name', 'address', 'phone')}),
    )


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('Tag Info'), {'fields': ('name', 'product')}),
    )


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('Review Info'), {'fields': ('product', 'customer', 'value')}),
    )

    readonly_fields = ('product', 'customer', 'value')


@admin.register(models.PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('Price History Info'), {'fields': ('product', 'price', 'start', 'end')}),
    )

    readonly_fields = ('start', 'end')
