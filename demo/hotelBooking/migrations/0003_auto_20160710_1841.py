# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0002_remove_product_shipping_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.IntegerField(max_length=255, default=1, verbose_name='product type', choices=[(1, '酒店订房')]),
        ),
    ]
