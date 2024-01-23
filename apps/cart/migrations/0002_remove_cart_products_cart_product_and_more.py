# Generated by Django 5.0.1 on 2024-01-23 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('products', '0004_alter_pricehistory_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ManyToManyField(blank=True, to='products.product'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='products',
            field=models.ManyToManyField(blank=True, to='products.product'),
        ),
    ]
