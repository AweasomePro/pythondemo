# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0019_remove_hotelpackageorder_snapshot'),
    ]

    operations = [
        migrations.RenameField(
            model_name='housepackage',
            old_name='room_avaliable',
            new_name='room_available',
        ),
    ]
