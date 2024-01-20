# Generated by Django 5.0.1 on 2024-01-20 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.supplier'),
        ),
        migrations.AlterField(
            model_name='product',
            name='average_review',
            field=models.FloatField(default=0.0),
        ),
    ]
