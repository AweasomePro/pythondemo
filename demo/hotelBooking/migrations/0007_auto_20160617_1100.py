# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0006_auto_20160616_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotellogoimg',
            name='hotel',
            field=models.ForeignKey(related_name='hotelLogoImgs', to='hotelBooking.Hotel'),
        ),
        migrations.AlterField(
            model_name='housepackage',
            name='house',
            field=models.ForeignKey(to='hotelBooking.House', verbose_name='房型', related_name='housepackages'),
        ),
    ]
