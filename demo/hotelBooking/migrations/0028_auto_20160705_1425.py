# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0027_auto_20160704_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='check_in_time',
            field=models.DateField(default='2016-07-05', verbose_name='入住时间'),
        ),
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='check_out_time',
            field=models.DateField(default='2016-07-06', verbose_name='离店时间'),
        ),
    ]
