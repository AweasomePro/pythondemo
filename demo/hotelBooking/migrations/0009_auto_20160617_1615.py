# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0008_auto_20160617_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houseimg',
            name='house',
            field=models.ForeignKey(related_name='houseImgs', verbose_name='房型', to='hotelBooking.House'),
        ),
    ]
