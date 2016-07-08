# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0033_auto_20160707_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentroomtypestate',
            name='city',
            field=models.ForeignKey(related_name='city_roomstates', to='hotelBooking.Hotel', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agentroomtypestate',
            name='hotel',
            field=models.ForeignKey(related_name='hotel_roomstates', to='hotelBooking.Hotel', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agentroomtypestate',
            name='housePackage',
            field=models.ForeignKey(related_name='house_roomstates', to='hotelBooking.HousePackage'),
        ),
    ]
