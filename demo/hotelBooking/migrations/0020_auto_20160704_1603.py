# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0018_auto_20160704_1559'),
    ]

    operations = [
        migrations.RenameField(
            model_name='housepackage',
            old_name='room_avaliable',
            new_name='room_available',
        ),
    ]
