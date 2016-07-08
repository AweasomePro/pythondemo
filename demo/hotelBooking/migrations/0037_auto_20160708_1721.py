# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0036_auto_20160707_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='agent',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='check_in_time',
            field=models.DateField(verbose_name='入住时间', default='2016-07-08'),
        ),
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='check_out_time',
            field=models.DateField(verbose_name='离店时间', default='2016-07-09'),
        ),
    ]
