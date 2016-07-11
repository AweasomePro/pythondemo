# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0003_auto_20160710_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='check_in_time',
            field=models.DateField(verbose_name='入住时间'),
        ),
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='check_out_time',
            field=models.DateField(verbose_name='离店时间'),
        ),
    ]
