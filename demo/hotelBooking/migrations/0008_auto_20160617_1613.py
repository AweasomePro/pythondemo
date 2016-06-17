# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0007_auto_20160617_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housepackage',
            name='house',
            field=models.ForeignKey(related_name='housePackages', to='hotelBooking.House', verbose_name='房型'),
        ),
    ]
