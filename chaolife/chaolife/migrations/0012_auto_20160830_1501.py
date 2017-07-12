# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0011_order_settled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelpackageorder',
            name='point_flow_to_seller',
        ),
        migrations.RemoveField(
            model_name='hotelpackageorder',
            name='point_flow_to_seller_count',
        ),
        migrations.RemoveField(
            model_name='hotelpackageorder',
            name='point_refund_to_customer_count',
        ),
    ]
