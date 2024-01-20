# Generated by Django 5.0.1 on 2024-01-20 01:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField()),
                ('sku', models.CharField(max_length=32)),
                ('category', models.IntegerField(choices=[(1, 'Science'), (2, 'Fiction'), (3, 'Journalism'), (4, 'Didactic')])),
                ('average_review', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('start', models.DateField(auto_now=True)),
                ('end', models.DateField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='customers',
            field=models.ManyToManyField(through='products.Review', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=11)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.product')),
            ],
        ),
    ]
