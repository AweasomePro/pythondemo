# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0009_auto_20160617_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housepackage',
            name='package_state',
            field=models.CharField(default='充沛', max_length=255, choices=[('1', '充沛'), ('2', '满房')]),
        ),
    ]
