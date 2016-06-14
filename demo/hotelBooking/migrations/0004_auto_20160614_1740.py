# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hotelBooking.helper.fiels


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0003_auto_20160614_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='introduce_imgs',
            field=hotelBooking.helper.fiels.ListField(null=True, blank=True),
        ),
    ]
