# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0034_auto_20160707_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentroomtypestate',
            name='housePackage',
            field=models.ForeignKey(related_name='housepackage_roomstates', to='hotelBooking.HousePackage'),
        ),
    ]
