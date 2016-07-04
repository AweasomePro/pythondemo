# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0021_hotelpackageordersnapshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, verbose_name='customer', to='hotelBooking.CustomerMember', blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='customer_orders'),
        ),
    ]
