# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0004_auto_20160710_1842'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotelpackageorder',
            options={'permissions': (('change_process_state', '能够操作改变订单过程状态'),)},
        ),
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.IntegerField(choices=[(1, '酒店订房')], default=1, verbose_name='product type'),
        ),
    ]
