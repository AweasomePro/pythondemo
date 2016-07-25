# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0006_hotel_cover_img'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotelimg',
            options={'verbose_name': '房间展示图片'},
        ),
    ]
