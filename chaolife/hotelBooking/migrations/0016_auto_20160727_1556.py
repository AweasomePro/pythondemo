# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0015_auto_20160727_1357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotelpackageorderitem',
            old_name='front_price',
            new_name='price',
        ),
    ]
