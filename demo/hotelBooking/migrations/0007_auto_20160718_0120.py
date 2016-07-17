# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0006_auto_20160717_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomdaystate',
            name='roomPackage',
            field=models.ForeignKey(related_name='roomstates', to='hotelBooking.RoomPackage'),
        ),
    ]
