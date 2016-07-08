# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0035_auto_20160707_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentroomtypestate',
            name='city',
            field=models.ForeignKey(to='hotelBooking.City', related_name='city_roomstates'),
        ),
    ]
