# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0032_auto_20160707_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentroomtypestate',
            name='housePackage',
            field=models.ForeignKey(related_name='house_roomstate', to='hotelBooking.HousePackage'),
        ),
    ]
