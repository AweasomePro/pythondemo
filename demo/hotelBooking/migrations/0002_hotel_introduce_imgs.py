# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hotelBooking.models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='introduce_imgs',
            field=hotelBooking.models.TestMultiModelField(default=''),
            preserve_default=False,
        ),
    ]
