# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0013_hotelpackageorder_process_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='housepackage',
            name='month_state',
        ),
        migrations.AddField(
            model_name='hotelpackageorder',
            name='check_in_time',
            field=models.DateField(verbose_name='入住时间', default=datetime.datetime(2016, 7, 4, 2, 18, 8, 405023, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotelpackageorder',
            name='check_out_time',
            field=models.DateField(verbose_name='离店时间', default=datetime.datetime(2016, 7, 4, 2, 18, 23, 505868, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotelpackageorder',
            name='extra_message',
            field=models.TextField(default=datetime.datetime(2016, 7, 4, 2, 19, 30, 902084, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='housepackage',
            name='room_avaliable',
            field=models.BigIntegerField(verbose_name='房态', default=0),
        ),
    ]
