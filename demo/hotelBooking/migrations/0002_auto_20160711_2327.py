# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotelpackageorder',
            options={'permissions': (('change_process_state', '能够操作改变订单过程状态'),)},
        ),
    ]
