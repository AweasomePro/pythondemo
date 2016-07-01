# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0003_auto_20160701_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='installation',
            name='valid',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='installation',
            name='installationId',
            field=models.CharField(max_length=200, verbose_name='设备id', null=True),
        ),
        migrations.AlterField(
            model_name='installation',
            name='timeZone',
            field=models.CharField(max_length=200, default=django.utils.timezone.now),
        ),
    ]
