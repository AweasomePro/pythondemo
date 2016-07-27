# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0013_auto_20160727_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomdaystate',
            name='d_price',
            field=models.IntegerField(default=0, verbose_name='当天双人前台现付价格'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='d_point',
            field=models.IntegerField(default=0, verbose_name='当天双人所需积分'),
        ),
        migrations.AlterField(
            model_name='roomdaystate',
            name='s_price',
            field=models.IntegerField(verbose_name='当天单人前台现付价格'),
        ),
        migrations.AlterField(
            model_name='roomdaystate',
            name='s_point',
            field=models.IntegerField(default=0, verbose_name='当天单人所需积分'),
        ),
    ]
