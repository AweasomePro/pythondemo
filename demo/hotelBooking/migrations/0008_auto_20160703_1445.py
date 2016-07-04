# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0007_hotelordernumbergenerator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_status',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_status',
        ),
    ]
