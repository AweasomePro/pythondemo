# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0009_auto_20160715_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='housepackage',
            name='active',
            field=models.BooleanField(verbose_name='是否可用 ?', default=False),
        ),
        migrations.AlterField(
            model_name='housepackage',
            name='checked',
            field=models.BooleanField(verbose_name='审核过 ?', default=False),
        ),
    ]
