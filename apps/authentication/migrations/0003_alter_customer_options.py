# Generated by Django 5.0.1 on 2024-01-23 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_customer_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['id'], 'verbose_name': 'Customer'},
        ),
    ]
