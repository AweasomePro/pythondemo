# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0022_auto_20160704_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_orders', null=True, verbose_name='customer', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
