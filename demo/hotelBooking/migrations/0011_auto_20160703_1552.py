# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0010_auto_20160703_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_status',
            field=models.IntegerField(choices=[(0, 'not shipped'), (1, 'not shipped'), (2, 'fully shipped')], verbose_name='shipping status', db_index=True, default=0),
        ),
    ]
