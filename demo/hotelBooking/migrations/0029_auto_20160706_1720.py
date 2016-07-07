# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotelBooking.core.exceptions


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0028_auto_20160705_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='check_in_time',
            field=models.DateField(verbose_name='入住时间', default='2016-07-06'),
        ),
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='check_out_time',
            field=models.DateField(verbose_name='离店时间', default='2016-07-07'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(verbose_name='password', max_length=128, validators=[hotelBooking.core.exceptions.UserCheck.validate_pwd]),
        ),
    ]
