# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0010_auto_20160726_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roompackage',
            name='default_s_point',
            field=models.IntegerField(verbose_name='默认单人所需积分', default=0),
        ),
        migrations.AlterField(
            model_name='roompackage',
            name='default_s_price',
            field=models.IntegerField(verbose_name='默认单人现付价格'),
        ),
    ]
