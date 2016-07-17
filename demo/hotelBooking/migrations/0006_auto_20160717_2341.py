# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0005_auto_20160717_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomdaystate',
            name='city',
            field=models.ForeignKey(related_name='roomstates', to='hotelBooking.City'),
        ),
        migrations.AlterField(
            model_name='roomdaystate',
            name='hotel',
            field=models.ForeignKey(related_name='roomstates', to='hotelBooking.Hotel'),
        ),
        migrations.AlterField(
            model_name='roomdaystate',
            name='roomPackage',
            field=models.ForeignKey(related_name='daystates', to='hotelBooking.RoomPackage'),
        ),
    ]
