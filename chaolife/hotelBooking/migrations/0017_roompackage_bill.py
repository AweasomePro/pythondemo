# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0016_auto_20160727_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='roompackage',
            name='bill',
            field=models.BooleanField(verbose_name='提供发票', default=True),
        ),
    ]
