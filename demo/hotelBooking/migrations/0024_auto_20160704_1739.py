# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0023_auto_20160704_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='customer_orders', verbose_name='customer', to=settings.AUTH_USER_MODEL, default=10000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.CharField(max_length=30, db_index=True, unique=True, blank=True, default=23454345678654567),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='product_orders', verbose_name='product', to='hotelBooking.Product', default=1),
            preserve_default=False,
        ),
    ]
