# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotelBooking.core.exceptions


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0004_auto_20160713_1134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agentroomtypestate',
            options={'verbose_name_plural': '房间类型状态', 'get_latest_by': 'date', 'verbose_name': '房间类型状态'},
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(validators=[hotelBooking.core.exceptions.UserCheck.validate_pwd], max_length=128, verbose_name='password'),
        ),
    ]
