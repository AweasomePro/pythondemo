# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import enumfields.fields
import hotelBooking.core.models.orders


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0008_auto_20160703_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=enumfields.fields.EnumIntegerField(default=1, db_index=True, verbose_name='payment status', enum=hotelBooking.core.models.orders.PaymentStatus),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_status',
            field=enumfields.fields.EnumIntegerField(default=0, db_index=True, verbose_name='shipping status', enum=hotelBooking.core.models.orders.ShippingStatus),
        ),
    ]
