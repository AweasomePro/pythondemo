# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0012_auto_20160727_1336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomdaystate',
            old_name='front_price',
            new_name='s_price',
        ),
        migrations.RenameField(
            model_name='roomdaystate',
            old_name='need_point',
            new_name='s_point',
        ),
    ]
