# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0006_auto_20160714_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='housepackage',
            name='checked',
            field=models.BooleanField(verbose_name='审核成功?', default=False),
        ),
    ]
