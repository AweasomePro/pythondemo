# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0011_auto_20160727_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='roompackage',
            name='default_d_point',
            field=models.IntegerField(default=0, verbose_name='默认双人所需积分'),
        ),
        migrations.AddField(
            model_name='roompackage',
            name='default_d_price',
            field=models.IntegerField(default=0, verbose_name='默认双人现付价格'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roompackage',
            name='price_type',
            field=models.IntegerField(choices=[(1, '单双同价'), (2, '单双异价')], default=1, verbose_name='价格类型'),
        ),
    ]
