# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0002_auto_20160722_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='Smoking',
            field=models.BooleanField(default=False, verbose_name='can smoke '),
        ),
    ]
