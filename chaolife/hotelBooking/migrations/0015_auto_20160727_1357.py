# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0014_auto_20160727_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelpackageorder',
            name='people_count',
            field=models.SmallIntegerField(default=1, verbose_name='入住人数'),
        ),
        migrations.AddField(
            model_name='hotelpackageorder',
            name='room_count',
            field=models.SmallIntegerField(default=1, verbose_name='房间件数'),
        ),
    ]
